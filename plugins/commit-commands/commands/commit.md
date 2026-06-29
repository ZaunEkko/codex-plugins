---
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*)
description: Create a git commit with Codex co-author attribution
---

## Context

Before committing, inspect the repository state:

- Current git status: !`git status --short`
- Current branch: !`git branch --show-current`
- Staged diff: !`git diff --cached`
- Unstaged diff: !`git diff`
- Recent commits: !`git log --oneline -10`

## Your task

Create exactly one git commit for the current staged and unstaged changes.

## Required behavior

1. Analyze both staged and unstaged changes.
2. Match the repository's existing commit style when possible.
3. Prefer Conventional Commits when the repository style is unclear.
4. Stage only relevant project files.
5. Do not stage or commit obvious secrets, credentials, local machine files, build artifacts, dependency folders, or generated cache directories.
6. Create a single commit.
7. Append this exact trailer to the commit message:

```text
Co-authored-by: Codex <noreply@openai.com>
```

## Secret and artifact guardrails

Never commit files matching obvious private or generated patterns, including but not limited to:

- `.env`, `.env.*`
- `*.pem`, `*.key`, `*.p12`, `*.pfx`
- `credentials.json`, `secrets.json`
- files containing API keys, tokens, passwords, or private keys
- `node_modules/`, `vendor/`, `bin/`, `obj/`, `dist/`, `build/`, `.godot/`, `.import/`
- logs, temporary files, IDE user state, and OS metadata files

If suspicious files are present, do not commit them. Commit the safe files only and report what was skipped.

## Execution rule

You have the capability to call multiple tools in a single response. Stage files and create the commit in one response. Do not edit files. Do not perform unrelated work. Do not send extra prose unless the commit cannot be safely created.
