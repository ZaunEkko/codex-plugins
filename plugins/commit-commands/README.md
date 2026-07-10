# Commit Commands with Dynamic Model and Effort Attribution

[简体中文](../../docs/commit-commands/README.md) · [English](../../i18n/en/docs/commit-commands/README.md) · [繁體中文](../../i18n/zh-TW/docs/commit-commands/README.md) · [日本語](../../i18n/ja/docs/commit-commands/README.md) · [한국어](../../i18n/ko/docs/commit-commands/README.md)

A Codex-native adaptation of Anthropic's original `commit-commands` plugin:

```text
$commit
$commit-push-pr
$clean-gone
```

The workflow steps follow the [Anthropic original](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/commit-commands). Codex-specific differences include native skill packaging, explicit-intent implicit selection, `$skill-name` invocation, and a `UserPromptSubmit` hook that provides the active Codex model and reasoning effort to the two commit-producing skills.

Review and trust the plugin hook with `/hooks` after installation or an update. Codex supplies the active model slug directly, but the current hook schema does not expose reasoning effort. The plugin therefore matches the current `turn_id` and model against the latest `turn_context` near the end of `transcript_path`, then falls back to `model_reasoning_effort` only when the user config targets the same model. It extracts only attribution fields and never copies or stores prompt content.

## Skills

### `$commit`

Inspects `git status`, `git diff HEAD`, the current branch, and the latest ten commits. It stages the current changes and creates exactly one commit with:

```text
Generated with [Codex](https://chatgpt.com/codex)
Model: <active-model-slug> <active-reasoning-effort>

Co-authored-by: Codex <noreply@openai.com>
```

The hook refreshes metadata for every user turn, including the first prompt after a model or effort change. Transcript parsing is isolated and best-effort because Codex does not guarantee that format. If effort cannot be resolved, the commit keeps only the model; if the model context is missing, the skill stops before staging or committing. It does not push or open a pull request. If there are no changes, it reports that instead of creating an empty commit.

### `$commit-push-pr`

Inspects the current status, diff, and branch. If the current branch is exactly `main`, it creates a new branch. It then creates exactly one commit, pushes the branch to `origin`, and opens a pull request with `gh pr create`.

This skill requires explicit PR intent. A commit-and-push-only request does not authorize PR creation. Like the original, it has no publish-without-a-new-commit path and does not create policy-driven branches for names other than `main`.

### `$clean-gone`

Uses `git branch -v` and `git worktree list` to find branches marked `[gone]`. For every candidate, it force-removes an associated non-main worktree with `git worktree remove --force`, then force-deletes the branch with `git branch -D`.

This deliberately matches the original destructive behavior. It does not fetch, verify merges, inspect worktree cleanliness, protect ignored files, or apply integration-branch rules. Review repository state before invoking it.

## Implicit invocation

- "Commit these changes" can select `commit`.
- "Commit these changes, push, and open a PR" can select `commit-push-pr`.
- "Clean all gone branches" can select `clean-gone`.
- "The implementation is finished" does not authorize any Git side effect.
