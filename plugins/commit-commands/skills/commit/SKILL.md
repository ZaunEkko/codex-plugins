---
name: commit
description: Create exactly one local Git commit from the current staged and unstaged changes, using recent history for message style and adding current-model Codex attribution. Use when the user explicitly asks to commit, save, record, or check in current changes. Do not use merely because implementation finished, and do not push or open a pull request.
---

# Commit

Adapt Anthropic's `/commit` workflow as a native Codex skill.

## Workflow

1. Inspect `git status`.
2. Inspect staged and unstaged changes with `git diff HEAD`.
3. Inspect the current branch with `git branch --show-current`.
4. Inspect the latest ten commits with `git log --oneline -10` and match the repository's commit-message style.
5. Read the active model slug from the `commit-commands runtime metadata for this turn` developer context injected by the plugin hook. Use the exact value; do not infer it from config, environment variables, or transcript files.
6. If that runtime metadata is missing or says the model is unavailable, stop before staging or committing. Tell the user to review and trust the plugin hook with `/hooks`, then retry in a new turn.
7. Based on the current changes, stage the relevant files.
8. Create exactly one commit with an appropriate message and append this attribution block:

```text
Generated with [Codex](https://chatgpt.com/codex)
Model: <active-model-slug>

Co-authored-by: Codex <noreply@openai.com>
```

9. Report the resulting commit and status.

## Boundaries

- If there are no changes to commit, report that instead of creating an empty commit.
- Never guess, hard-code, or retain a stale model slug.
- Avoid staging obvious secrets such as `.env` or credential files.
- Do not push, open a pull request, amend an existing commit, or perform unrelated work.
