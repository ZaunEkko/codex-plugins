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

1. If currently on `main` or `master`, create a new feature branch first.
2. Analyze staged and unstaged changes.
3. Stage only relevant project files.
4. Skip local-only files, generated output, dependency folders, caches, logs, and environment/config files that do not belong in the repository.
5. Create exactly one commit for the current changes.
6. Append this exact trailer to the commit message:

```text
Co-authored-by: Codex <noreply@openai.com>
```

7. Publish the current branch to `origin`.
8. Open a pull request with the GitHub CLI.
9. Include a concise pull request description with Summary, Test plan, Notes/risks if relevant, and Codex attribution.

## PR attribution

Include this exact line in the PR body:

```text
Generated with Codex assistance.
```

## Execution rule

Complete the branch, commit, publish, and pull request workflow in one response. Do not edit files. Do not perform unrelated work. Do not send extra prose unless the workflow cannot be safely completed.
