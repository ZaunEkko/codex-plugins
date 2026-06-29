import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "commit-commands"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"


class CommitCommandsPluginTests(unittest.TestCase):
    def test_plugin_manifest_exists_and_exposes_commands(self):
        manifest = json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "commit-commands")
        self.assertIn("Commands", manifest["interface"]["capabilities"])

    def test_commands_are_present(self):
        commands = PLUGIN_ROOT / "commands"
        self.assertTrue((commands / "commit.md").is_file())
        self.assertTrue((commands / "commit-push-pr.md").is_file())
        self.assertTrue((commands / "clean_gone.md").is_file())

    def test_codex_attribution_is_configured(self):
        text = (PLUGIN_ROOT / "commands" / "commit.md").read_text(encoding="utf-8")
        self.assertIn("noreply@openai.com", text)

    def test_commit_push_pr_protects_integration_branches(self):
        text = (PLUGIN_ROOT / "commands" / "commit-push-pr.md").read_text(encoding="utf-8")
        self.assertIn("`dev`", text)
        self.assertIn("repository-local workflow instructions", text)
        self.assertIn("Never commit or push directly to a protected branch", text)
        self.assertIn("repository-required integration branch", text)

    def test_clean_gone_preserves_unsafe_candidates(self):
        text = (PLUGIN_ROOT / "commands" / "clean_gone.md").read_text(encoding="utf-8")
        self.assertIn("git merge-base --is-ancestor", text)
        self.assertIn("git -C <worktree-path> status --short", text)
        self.assertIn("git branch -d <branch>", text)
        self.assertNotIn("git branch -D", text)
        self.assertNotIn("worktree remove --force", text)
        self.assertIn("skip the branch as unmerged", text)

    def test_marketplace_registers_plugin(self):
        marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        plugins = {plugin["name"]: plugin for plugin in marketplace["plugins"]}
        self.assertIn("commit-commands", plugins)


if __name__ == "__main__":
    unittest.main()
