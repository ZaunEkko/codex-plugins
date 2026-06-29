---
name: commit
description: Create exactly one safe local Git commit for the current task while following repository instructions, matching commit style, screening secrets and artifacts, and adding Codex co-author attribution. Use when the user explicitly asks to commit, save, record, or check in current changes. Do not use merely because implementation finished, and do not push or open a pull request.
---

# Commit

Create one focused local commit without modifying unrelated files or publishing the branch.

## Workflow

1. Read repository instructions such as `AGENTS.md` and `CONTRIBUTING.md`. Obey branch, validation, staging, and commit-message rules.
2. Inspect the current branch, worktree, index, unstaged diff, staged diff, and recent commit history.
3. If there are no safe relevant changes, do not create an empty commit; report why no commit was created.
4. Identify files that belong to the current task. Exclude suspicious or unrelated files.
5. Run required validation when repository instructions require it before committing.
6. Stage only the selected files, then inspect the staged diff again.
7. Create exactly one commit using the repository's established message style. If no style is clear, use a concise Conventional Commit.
8. Append this exact trailer to the commit message:

```text
Co-authored-by: Codex <noreply@openai.com>
```

9. Report the commit hash, subject, validation performed, and any files intentionally skipped.

## Safety rules

- Stop if repository policy forbids committing on the current branch. Do not silently switch branches, stash, reset, or rebase.
- Never stage obvious credentials, private keys, `.env` files, tokens, passwords, machine-local files, dependency directories, build output, caches, logs, or editor state.
- Treat unusual generated or binary files as suspicious unless repository instructions or the task clearly require them.
- Do not amend an existing commit unless the user explicitly asks.
- Do not push, open a pull request, or perform unrelated work.
