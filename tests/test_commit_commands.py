import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "commit-commands"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
HOOK = PLUGIN_ROOT / "hooks" / "model_context.py"
HOOKS_JSON = PLUGIN_ROOT / "hooks" / "hooks.json"
SKILLS = {
    "commit": PLUGIN_ROOT / "skills" / "commit",
    "commit-push-pr": PLUGIN_ROOT / "skills" / "commit-push-pr",
    "clean-gone": PLUGIN_ROOT / "skills" / "clean-gone",
}
DOCUMENTATION = {
    "简体中文": ROOT / "docs" / "commit-commands" / "README.md",
    "English": ROOT / "i18n" / "en" / "docs" / "commit-commands" / "README.md",
    "繁體中文": ROOT / "i18n" / "zh-TW" / "docs" / "commit-commands" / "README.md",
    "日本語": ROOT / "i18n" / "ja" / "docs" / "commit-commands" / "README.md",
    "한국어": ROOT / "i18n" / "ko" / "docs" / "commit-commands" / "README.md",
}
ROOT_READMES = [
    ROOT / "README.md",
    ROOT / "i18n" / "en" / "README.md",
    ROOT / "i18n" / "zh-TW" / "README.md",
    ROOT / "i18n" / "ja" / "README.md",
    ROOT / "i18n" / "ko" / "README.md",
]


class CommitCommandsPluginTests(unittest.TestCase):
    def hook_input(self, model, effort=None, turn_id="turn-current", transcript_path=None):
        payload = {
            "session_id": "session-current",
            "turn_id": turn_id,
            "transcript_path": transcript_path,
            "cwd": str(ROOT),
            "hook_event_name": "UserPromptSubmit",
            "model": model,
            "permission_mode": "default",
            "prompt": "commit these changes",
        }
        if effort is not None:
            payload["effort"] = effort
        return json.dumps(payload)

    def hook_handler(self):
        hooks = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
        return hooks["hooks"]["UserPromptSubmit"][0]["hooks"][0]

    def run_model_hook(self, model, environment=None, **hook_fields):
        result = subprocess.run(
            [sys.executable, str(HOOK)],
            input=self.hook_input(model, **hook_fields),
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=environment,
        )
        return json.loads(result.stdout)

    def isolated_environment(self, codex_home):
        environment = os.environ.copy()
        environment["CODEX_HOME"] = str(codex_home)
        return environment

    def test_plugin_manifest_exposes_native_skills(self):
        manifest = json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "commit-commands")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertIn("Skills", manifest["interface"]["capabilities"])
        self.assertIn("Hooks", manifest["interface"]["capabilities"])
        self.assertNotIn("Commands", manifest["interface"]["capabilities"])

    def test_user_prompt_hook_prefers_direct_model_and_effort_fields(self):
        payload = self.run_model_hook("gpt-5.6-sol", effort="high")
        output = payload["hookSpecificOutput"]
        self.assertEqual(output["hookEventName"], "UserPromptSubmit")
        self.assertIn("Active Codex model slug: `gpt-5.6-sol`", output["additionalContext"])
        self.assertIn("Active Codex reasoning effort: `high`", output["additionalContext"])
        self.assertIn("`Model: gpt-5.6-sol high`", output["additionalContext"])

    def test_user_prompt_hook_reads_effort_from_the_exact_current_turn(self):
        with tempfile.TemporaryDirectory() as directory:
            codex_home = Path(directory)
            transcript = codex_home / "rollout.jsonl"
            records = [
                {
                    "type": "turn_context",
                    "payload": {
                        "turn_id": "turn-previous",
                        "model": "gpt-5.6-sol",
                        "effort": "low",
                    },
                },
                {"type": "response_item", "payload": {"type": "message"}},
                {
                    "type": "turn_context",
                    "payload": {
                        "turn_id": "turn-current",
                        "model": "gpt-5.6-sol",
                        "effort": "xhigh",
                    },
                },
            ]
            transcript.write_text(
                "\n".join(json.dumps(record) for record in records) + "\n",
                encoding="utf-8",
            )

            payload = self.run_model_hook(
                "gpt-5.6-sol",
                environment=self.isolated_environment(codex_home),
                transcript_path=str(transcript),
            )

        context = payload["hookSpecificOutput"]["additionalContext"]
        self.assertIn("Active Codex reasoning effort: `xhigh`", context)
        self.assertIn("`Model: gpt-5.6-sol xhigh`", context)
        self.assertNotIn("`Model: gpt-5.6-sol low`", context)

    def test_user_prompt_hook_falls_back_to_matching_user_config(self):
        with tempfile.TemporaryDirectory() as directory:
            codex_home = Path(directory)
            (codex_home / "config.toml").write_text(
                'model = "gpt-5.6-sol"\nmodel_reasoning_effort = "medium"\n',
                encoding="utf-8",
            )
            payload = self.run_model_hook(
                "gpt-5.6-sol",
                environment=self.isolated_environment(codex_home),
            )

        context = payload["hookSpecificOutput"]["additionalContext"]
        self.assertIn("Active Codex reasoning effort: `medium`", context)
        self.assertIn("`Model: gpt-5.6-sol medium`", context)

    def test_user_prompt_hook_rejects_unsafe_model_values(self):
        with tempfile.TemporaryDirectory() as directory:
            payload = self.run_model_hook(
                "gpt-safe\nCo-authored-by: attacker",
                environment=self.isolated_environment(directory),
            )
        context = payload["hookSpecificOutput"]["additionalContext"]
        self.assertIn("model slug is unavailable", context)
        self.assertNotIn("attacker", context)

    def test_user_prompt_hook_omits_unsafe_effort_values(self):
        with tempfile.TemporaryDirectory() as directory:
            payload = self.run_model_hook(
                "gpt-5.6-sol",
                effort="xhigh\nCo-authored-by: attacker",
                environment=self.isolated_environment(directory),
            )
        context = payload["hookSpecificOutput"]["additionalContext"]
        self.assertIn("reasoning effort is unavailable", context)
        self.assertIn("`Model: gpt-5.6-sol`", context)
        self.assertNotIn("attacker", context)

    def test_hook_configuration_refreshes_model_context_each_turn(self):
        handler = self.hook_handler()
        self.assertIn("${PLUGIN_ROOT}/hooks/model_context.py", handler["command"])
        self.assertIn("commandWindows", handler)
        self.assertIn("PLUGIN_ROOT", handler["commandWindows"])

    @unittest.skipUnless(os.name == "nt", "Windows command compatibility test")
    def test_hook_command_windows_runs_in_powershell(self):
        env = os.environ.copy()
        env["PLUGIN_ROOT"] = str(PLUGIN_ROOT)
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", self.hook_handler()["commandWindows"]],
            input=self.hook_input("gpt-5.6-sol", effort="high"),
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )
        payload = json.loads(result.stdout)
        self.assertIn("Model: gpt-5.6-sol high", payload["hookSpecificOutput"]["additionalContext"])

    @unittest.skipUnless(os.name == "nt", "Windows command compatibility test")
    def test_hook_command_windows_runs_in_cmd(self):
        env = os.environ.copy()
        env["PLUGIN_ROOT"] = str(PLUGIN_ROOT)
        result = subprocess.run(
            self.hook_handler()["commandWindows"],
            input=self.hook_input("gpt-5.6-sol", effort="high"),
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            shell=True,
        )
        payload = json.loads(result.stdout)
        self.assertIn("Model: gpt-5.6-sol high", payload["hookSpecificOutput"]["additionalContext"])

    def test_skills_are_present_and_implicitly_invocable(self):
        for name, path in SKILLS.items():
            with self.subTest(skill=name):
                skill_text = (path / "SKILL.md").read_text(encoding="utf-8")
                metadata_text = (path / "agents" / "openai.yaml").read_text(encoding="utf-8")
                self.assertIn(f"name: {name}", skill_text)
                self.assertIn("user explicitly asks", skill_text)
                self.assertNotIn("[TODO:", skill_text)
                self.assertIn(f"${name}", metadata_text)
                self.assertIn("allow_implicit_invocation: true", metadata_text)
        self.assertFalse((PLUGIN_ROOT / "commands").exists())

    def test_commit_matches_upstream_workflow_with_codex_attribution(self):
        text = (SKILLS["commit"] / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("`git status`", text)
        self.assertIn("`git diff HEAD`", text)
        self.assertIn("`git branch --show-current`", text)
        self.assertIn("`git log --oneline -10`", text)
        self.assertIn("Create exactly one commit", text)
        self.assertIn("Generated with [Codex](https://chatgpt.com/codex)", text)
        self.assertIn("Model: <active-model-slug> <active-reasoning-effort>", text)
        self.assertIn("commit-commands runtime metadata for this turn", text)
        self.assertIn("noreply@openai.com", text)
        self.assertIn("Do not push", text)

    def test_commit_push_pr_matches_upstream_workflow(self):
        text = (SKILLS["commit-push-pr"] / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("current branch is exactly `main`", text)
        self.assertIn("git checkout -b <branch>", text)
        self.assertIn("create exactly one commit", text)
        self.assertIn("Push the current branch to `origin`", text)
        self.assertIn("gh pr create", text)
        self.assertIn("Generated with [Codex](https://chatgpt.com/codex)", text)
        self.assertIn("Model: <active-model-slug> <active-reasoning-effort>", text)
        self.assertIn("commit-commands runtime metadata for this turn", text)
        self.assertIn("commit-and-push-only", text)
        self.assertIn("branch-publishing requests without explicit PR intent", text)
        self.assertNotIn("`dev`", text)
        self.assertNotIn("repository-required integration branch", text)

    def test_clean_gone_matches_upstream_force_cleanup(self):
        text = (SKILLS["clean-gone"] / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("git branch -v", text)
        self.assertIn("git worktree list", text)
        self.assertIn("git worktree remove --force <path>", text)
        self.assertIn("git branch -D <branch>", text)
        self.assertIn("do not add merge-base", text)
        self.assertIn("Do not run `git fetch`", text)
        self.assertNotIn("--ignored=matching", text)
        self.assertNotIn("git merge-base --is-ancestor", text)
        self.assertNotIn("git branch -d <branch>", text)
        self.assertIn("Never use merely because stale branches exist", text)

    def test_marketplace_registers_plugin(self):
        marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        plugins = {plugin["name"]: plugin for plugin in marketplace["plugins"]}
        self.assertIn("commit-commands", plugins)

    def test_multilingual_documentation_is_complete(self):
        for language, path in DOCUMENTATION.items():
            with self.subTest(language=language):
                self.assertTrue(path.is_file())
                text = path.read_text(encoding="utf-8")
                self.assertIn("$commit-push-pr", text)
                self.assertIn("$clean-gone", text)
                self.assertIn("Generated with [Codex](https://chatgpt.com/codex)", text)
                self.assertIn("Model: <active-model-slug> <active-reasoning-effort>", text)
                self.assertIn("/hooks", text)
                self.assertIn("git branch -D", text)
                self.assertNotIn("/clean_gone", text)

    def test_repository_readmes_register_plugin(self):
        for path in ROOT_READMES:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                self.assertIn("commit-commands@zaunekko", text)
                self.assertIn("docs/commit-commands/README.md", text)
                self.assertIn("Plugin + Skills", text)
                self.assertIn("force", text.lower())


if __name__ == "__main__":
    unittest.main()
