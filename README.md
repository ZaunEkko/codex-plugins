# Codex Plugins

Personal Codex plugin marketplace.

## Plugins

- `explanatory-output-style`: Adds brief educational implementation insights at Codex session start.

## Install

After this repository is pushed to GitHub, users can add the marketplace and install the plugin:

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
codex plugin add explanatory-output-style@zaunekko
```

Because this plugin uses a `SessionStart` hook, Codex will ask each user to review and trust the hook once in `/hooks`.
