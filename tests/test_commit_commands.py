import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "commit-commands"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
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
    def test_plugin_manifest_exposes_native_skills(self):
        manifest = json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "commit-commands")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertIn("Skills", manifest["interface"]["capabilities"])
        self.assertNotIn("Commands", manifest["interface"]["capabilities"])

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
        self.assertIn("noreply@openai.com", text)
        self.assertIn("Do not push", text)

    def test_commit_push_pr_matches_upstream_workflow(self):
        text = (SKILLS["commit-push-pr"] / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("current branch is exactly `main`", text)
        self.assertIn("git checkout -b <branch>", text)
        self.assertIn("create exactly one commit", text)
        self.assertIn("Push the current branch to `origin`", text)
        self.assertIn("gh pr create", text)
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
