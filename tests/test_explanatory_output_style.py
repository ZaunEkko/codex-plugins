import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "explanatory-output-style"
HOOK = PLUGIN_ROOT / "hooks" / "session_start.py"
HOOKS_JSON = PLUGIN_ROOT / "hooks" / "hooks.json"


class ExplanatoryOutputStyleTests(unittest.TestCase):
    def hook_context(self):
        result = subprocess.run(
            [sys.executable, str(HOOK)],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        payload = json.loads(result.stdout)
        return payload["hookSpecificOutput"]["additionalContext"]

    def command_windows(self):
        hooks = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
        return hooks["hooks"]["SessionStart"][0]["hooks"][0]["commandWindows"]

    def run_command_windows(self, shell_command, **kwargs):
        env = os.environ.copy()
        env["PLUGIN_ROOT"] = str(PLUGIN_ROOT)
        result = subprocess.run(
            shell_command,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            **kwargs,
        )
        return json.loads(result.stdout)

    def test_insight_block_uses_left_border_only_to_avoid_wrapping_artifacts(self):
        context = self.hook_context()
        opening_line = "`+-------------------- ★ Insight --------------------+`"
        closing_line = "`+---------------------------------------------------+`"
        bullet_placeholder_line = "| [2-3 concise bullets]"

        self.assertIn(opening_line, context)
        self.assertIn(closing_line, context)
        self.assertIn(bullet_placeholder_line, context)
        self.assertIn("\n\n" + opening_line, context)
        self.assertIn("Start the block with a blank line before the opening divider.", context)
        self.assertIn("Use only the left `|` on bullet lines; do not add a trailing right `|`.", context)
        self.assertTrue(closing_line.strip("`").isascii())

    @unittest.skipUnless(os.name == "nt", "Windows command compatibility test")
    def test_command_windows_runs_in_powershell(self):
        payload = self.run_command_windows(
            ["powershell", "-NoProfile", "-Command", self.command_windows()]
        )

        self.assertEqual(payload["hookSpecificOutput"]["hookEventName"], "SessionStart")

    @unittest.skipUnless(os.name == "nt", "Windows command compatibility test")
    def test_command_windows_runs_in_cmd(self):
        payload = self.run_command_windows(
            self.command_windows(),
            shell=True,
        )

        self.assertEqual(payload["hookSpecificOutput"]["hookEventName"], "SessionStart")


if __name__ == "__main__":
    unittest.main()
