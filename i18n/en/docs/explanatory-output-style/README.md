# explanatory-output-style

[简体中文](../../../../docs/explanatory-output-style/README.md) · [English](README.md) · [繁體中文](../../../zh-TW/docs/explanatory-output-style/README.md) · [日本語](../../../ja/docs/explanatory-output-style/README.md) · [한국어](../../../ko/docs/explanatory-output-style/README.md)

`explanatory-output-style` is a Codex plugin that enables an explanatory output style in Codex sessions.

It follows the experience of Claude Code's official [`explanatory-output-style`](https://github.com/anthropics/claude-code/tree/main/plugins/explanatory-output-style) plugin: a `SessionStart` hook injects extra guidance at the beginning of a session so the model adds short, codebase-specific Insight notes when writing or changing code.

## When to use it

- You want Codex to explain implementation choices, not just produce the final change.
- You want a team to share the same "explain while working" collaboration style.
- You want to distribute an output style as an installable plugin instead of copying prompts into every project.

## Relationship to the official Claude Code plugin

The official Claude Code plugin uses a `SessionStart` hook to add explanatory output guidance at session start. This repository adapts that behavior for the Codex plugin system:

- Codex plugin manifest: `plugins/explanatory-output-style/.codex-plugin/plugin.json`
- Codex hook configuration: `plugins/explanatory-output-style/hooks/hooks.json`
- Python hook that emits the JSON payload Codex expects: `hookSpecificOutput.additionalContext`
- Separate Windows / Unix hook commands for cross-platform installation

## Collaboration behavior after injection

The injected context asks Codex to:

1. Provide short Insight notes before and after writing or changing code.
2. Focus on implementation choices, project conventions, and tradeoffs in the current codebase.
3. Avoid generic tutorials or long explanations of general programming concepts.
4. Use a narrow-terminal-friendly output block format to reduce wrapping and border misalignment.

Current Insight block example:

```text
`+-------------------- ★ Insight --------------------+`
| 2-3 short bullets explaining the current implementation choice
`+---------------------------------------------------+`
```

Bullet lines keep only the left `|` and do not add a right border, which prevents border misalignment when terminals wrap text.

## Installation and enablement

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
codex plugin add explanatory-output-style@zaunekko
```

Before first use, review and trust command hooks in Codex:

```text
/hooks
```

Review:

- The actual command in `hooks/hooks.json`.
- Whether `hooks/session_start.py` only emits the expected JSON.
- Hook output should not contain API keys, tokens, machine-specific paths, or other sensitive information.

## Local validation

Run from the repository root:

```bash
python -m py_compile plugins/explanatory-output-style/hooks/session_start.py
python plugins/explanatory-output-style/hooks/session_start.py
python -m unittest tests.test_explanatory_output_style
codex plugin list
```

The first three commands validate Python syntax, hook JSON payload, and plugin output format. `codex plugin list` confirms Codex can discover the marketplace plugin.
