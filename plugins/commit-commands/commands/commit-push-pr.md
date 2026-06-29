---
description: Commit changes, publish the current branch, and open a pull request
---

## Context

Inspect the repository state before starting:

- Current git status: !`git status --short`
- Current branch: !`git branch --show-current`
- Staged diff: !`git diff --cached`
- Unstaged diff: !`git diff`
- Recent commits: !`git log --oneline --decorate --max-count=20`

## Your task

Create a single commit for the current safe changes, publish the current work branch, and open a pull request.

## Required behavior

1. Inspect repository-local workflow instructions such as `AGENTS.md` and `CONTRIBUTING.md` when present. Follow their branch naming, base branch, commit, and validation rules.
2. Treat `main`, `master`, `dev`, `develop`, and any branch designated as protected or integration-only by repository instructions as protected branches.
3. If currently on a protected branch, create a compliant work branch from the repository-required base before committing. Never commit or push directly to a protected branch.
4. If moving the work to the required base cannot be done without risking current changes, stop and explain the conflict. Do not reset, stash, or rebase without explicit user approval.
5. Analyze staged and unstaged changes.
6. Stage only relevant project files.
7. Skip local-only files, generated output, dependency folders, caches, logs, and environment/config files that do not belong in the repository.
8. Create exactly one commit for the current changes.
9. Append this exact trailer to the commit message:

```text
Co-authored-by: Codex <noreply@openai.com>
```

10. Re-check that the current branch is a compliant work branch before publishing it to `origin`.
11. Open a pull request against the repository-required integration branch with the GitHub CLI.
12. Include a concise pull request description with Summary, Test plan, Notes/risks if relevant, and Codex attribution.

## PR attribution

Include this exact line in the PR body:

```text
Generated with Codex assistance.
```

## Execution rule

Complete the branch, commit, publish, and pull request workflow in one response. Do not edit files. Do not perform unrelated work. Do not send extra prose unless the workflow cannot be safely completed.
