---
name: commit-push-pr
description: Commit safe current changes, publish a compliant work branch to origin, and open a pull request with GitHub CLI while following repository branch policy. Use when the user explicitly asks to commit and push, publish a branch, create or open a PR, or complete the commit-push-PR workflow. Do not use for commit-only requests or without explicit publishing intent.
---

# Commit, Push, and Open PR

Complete the repository-aware branch, commit, publish, and pull request workflow without bypassing local policy.

## Workflow

1. Read repository instructions such as `AGENTS.md` and `CONTRIBUTING.md`. Identify naming rules, the required base and integration branch, protected branches, validation commands, commit style, and PR requirements.
2. Inspect the current branch, worktree, index, staged and unstaged diffs, recent commits, remotes, and GitHub CLI availability.
3. Treat `main`, `master`, `dev`, `develop`, and every repository-designated protected or integration-only branch as protected.
4. If currently on a protected branch, create a compliant work branch from the repository-required base before committing. Preserve current changes only when the branch switch is safe.
5. If the required base or branch transition is ambiguous or risks current work, stop and explain the conflict. Do not reset, stash, rebase, or discard changes without explicit approval.
6. Identify safe files relevant to the current task, run required validation, stage only those files, and inspect the staged diff.
7. Create exactly one commit using the repository's established style and append:

```text
Co-authored-by: Codex <noreply@openai.com>
```

8. Re-check that the current branch is a compliant work branch, then publish it to `origin` without force pushing.
9. Open a pull request against the repository-required integration branch with GitHub CLI.
10. Write a concise PR body containing Summary, Test plan, Notes or risks when relevant, and this exact attribution:

```text
Generated with Codex assistance.
```

11. Report the branch, commit, PR URL, validation performed, and any skipped files.

## Safety rules

- Never commit or push directly to a protected or integration-only branch.
- Never force push, bypass required checks, overwrite remote history, or silently move changes across a risky branch transition.
- Never stage obvious credentials, private keys, `.env` files, tokens, passwords, machine-local files, dependency directories, build output, caches, logs, or editor state.
- Stop before publishing if `origin`, GitHub CLI authentication, the target branch, or repository policy cannot be verified.
- Do not edit unrelated files or perform unrelated work.
