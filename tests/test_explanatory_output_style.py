import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "plugins" / "explanatory-output-style" / "hooks" / "session_start.py"


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

    def test_insight_block_uses_ascii_box_with_star_in_top_border(self):
        context = self.hook_context()
        opening_line = "`+-------------------- ★ Insight --------------------+`"
        closing_line = "`+---------------------------------------------------+`"
        bullet_placeholder_line = "| [2-3 concise bullets]"

        self.assertIn(opening_line, context)
        self.assertIn(closing_line, context)
        self.assertIn(bullet_placeholder_line, context)
        self.assertIn("\n\n" + opening_line, context)
        self.assertIn("Start the block with a blank line before the opening divider.", context)
        self.assertTrue(closing_line.strip("`").isascii())


if __name__ == "__main__":
    unittest.main()
