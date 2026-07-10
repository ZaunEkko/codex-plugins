---
name: commit-push-pr
description: Create a branch when currently on main, create exactly one current-model-and-reasoning-effort-attributed commit, push the branch to origin, and open a pull request with GitHub CLI. Use only when the user explicitly asks to create or open a pull request, or explicitly requests the full commit-push-PR workflow. Do not use for commit-only, commit-and-push-only, or branch-publishing requests without explicit PR intent.
---

# Commit, Push, and Open PR

Adapt Anthropic's `/commit-push-pr` workflow as a native Codex skill.

## Workflow

1. Inspect `git status`, the staged and unstaged changes with `git diff HEAD`, and the current branch with `git branch --show-current`.
2. Read the active model slug and optional reasoning effort from the `commit-commands runtime metadata for this turn` developer context injected by the plugin hook. Use the exact `Model:` line provided there; do not independently infer it from config, environment variables, or transcript files.
3. If that runtime metadata is missing or says the model is unavailable, stop before creating a branch, staging, or committing. Tell the user to review and trust the plugin hook with `/hooks`, then retry in a new turn.
4. If the current branch is exactly `main`, create a new work branch with `git checkout -b <branch>`.
5. Stage the current changes and create exactly one commit with an appropriate message. Append this attribution block:

```text
Generated with [Codex](https://chatgpt.com/codex)
Model: <active-model-slug> <active-reasoning-effort>

Co-authored-by: Codex <noreply@openai.com>
```

   If the runtime metadata says reasoning effort is unavailable, omit only the effort suffix and keep `Model: <active-model-slug>`.
6. Push the current branch to `origin`.
7. Create a pull request with `gh pr create`.
8. Describe the full branch in the PR body with a 1–3 bullet summary, a test-plan checklist, and:

```text
Generated with Codex assistance.
```

9. Return the pull request URL.

## Boundaries

- Complete commit, push, and PR creation as one workflow; do not turn this into a push-only or PR-only path.
- If there are no changes to commit, report that the original workflow cannot continue instead of creating an empty commit.
- Never guess, hard-code, or retain a stale model slug or reasoning effort.
- Create a new branch automatically only when the current branch is `main`; do not add other policy-driven branch transitions to the original workflow.
- Never force push, stage obvious secrets, or perform unrelated work.
- Stop if GitHub CLI is unavailable or unauthenticated, or if `origin` is missing.
