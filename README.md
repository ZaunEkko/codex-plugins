# Codex Plugins

Small Codex plugins for sharper local workflows.

This repo is a personal marketplace for Codex extensions that change how a
session feels, starts, or connects to project context.

## Plugins

- `explanatory-output-style`

  Brings an explanatory working style into Codex sessions. On session start, the
  plugin injects guidance that nudges Codex to explain implementation choices
  with compact, codebase-specific insight blocks while it works.

## Install

Add this marketplace, then install the plugin:

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
codex plugin add explanatory-output-style@zaunekko
```

## Trust

This plugin uses a `SessionStart` hook. Codex will ask each user to review and
trust the hook once in `/hooks` before it runs.

## Use

Start a new Codex thread after installation. The plugin activates at session
startup, resume, clear, and compact events.
