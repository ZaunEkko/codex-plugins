<div align="center">

# 🧩 Codex Plugins

### A personal marketplace for Codex workflows

*Package useful plugins, skills, hooks, and output styles so others can install them too.*

[简体中文](../../README.md) · [English](README.md) · [繁體中文](../zh-TW/README.md) · [日本語](../ja/README.md) · [한국어](../ko/README.md)

</div>

---

## ✨ What is this repository?

This repository is a personal Codex workflow marketplace. It collects reusable Codex customization units: plugins, skills, hooks, startup context, output styles, and development workflows.

The goal is to package useful Codex configurations so other people can install, enable, and reuse them directly.

## 📦 Current plugins

| Plugin | Type | Description | Docs |
|--------|------|-------------|------|
| explanatory-output-style | Plugin + SessionStart Hook | Ports the official Claude Code explanatory-output-style experience to Codex. | [Plugin docs](docs/explanatory-output-style/README.md) |
| commit-commands | Plugin + Skills + UserPromptSubmit Hook | Attributes commits, verifies `Generated with [Codex](https://chatgpt.com/codex)` in GitHub.com/GitHub Enterprise PR bodies, and preserves force cleanup. | [Plugin docs](docs/commit-commands/README.md) |

## 🚀 Quick start

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
codex plugin add explanatory-output-style@zaunekko
codex plugin add commit-commands@zaunekko
```

Plugins with command hooks must be reviewed and trusted in Codex before first use:

```text
/hooks
```

## 📚 Plugin documentation

- [explanatory-output-style](docs/explanatory-output-style/README.md): feature, installation, hook trust, and local validation notes.
- [commit-commands](docs/commit-commands/README.md): commit, pull request publishing, branch cleanup, safeguards, and local validation notes.

## 🧪 Local validation

```bash
codex plugin list
python -m py_compile plugins/explanatory-output-style/hooks/session_start.py
python plugins/explanatory-output-style/hooks/session_start.py
python -m unittest discover -s tests
```

## ⚠️ Trust & Safety

- Read plugin docs before installing.
- Review command hooks in `/hooks`.
- Re-trust hooks after changing them.
- Review repository state before triggering skills that commit, push, or delete branches.
- Do not write API keys, tokens, passwords, or machine-specific paths into hook output.

## 📄 License

This project is open source under the [MIT License](../../LICENSE).

## 🤝 Community

- [Contributing](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
