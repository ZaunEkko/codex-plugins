import json
import subprocess
import sys
import unicodedata
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "plugins" / "explanatory-output-style" / "hooks" / "session_start.py"


def terminal_width(text):
    width = 0
    for char in text:
        if char == "★":
            width += 2
        elif unicodedata.east_asian_width(char) in {"F", "W"}:
            width += 2
        else:
            width += 1
    return width


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

    def test_insight_block_uses_aligned_dividers_with_leading_blank_line(self):
        context = self.hook_context()
        opening_line = "`────────────────── ★ Insight ──────────────────`"
        closing_line = "`────────────────────────────────────────────────`"

        self.assertIn(opening_line, context)
        self.assertIn(closing_line, context)
        self.assertIn("\n\n" + opening_line, context)
        self.assertIn("Start the block with a blank line before the opening divider.", context)
        self.assertEqual(
            terminal_width(opening_line.strip("`")),
            terminal_width(closing_line.strip("`")),
        )


if __name__ == "__main__":
    unittest.main()
