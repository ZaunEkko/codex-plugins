# commit-commands

[简体中文](../../../../docs/commit-commands/README.md) · [English](README.md) · [繁體中文](../../../zh-TW/docs/commit-commands/README.md) · [日本語](../../../ja/docs/commit-commands/README.md) · [한국어](../../../ko/docs/commit-commands/README.md)

`commit-commands` adapts the three slash commands from the [official Anthropic original](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/commit-commands) as native Codex skills:

```text
$commit
$commit-push-pr
$clean-gone
```

Workflow steps follow the original. Codex-specific differences include native skill packaging, explicit-intent implicit selection, `$skill-name` invocation, and a `UserPromptSubmit` hook that dynamically provides the active Codex model and reasoning effort for commit attribution.

## Installation

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
codex plugin add commit-commands@zaunekko
```

After installing or updating, review and trust the `commit-commands` hook with `/hooks`, then start a new Codex thread so the new skill and hook metadata is loaded.

## Implicit selection examples

- "Commit these changes" can select `commit`.
- "Commit these changes, push, and open a PR" can select `commit-push-pr`.
- "Clean all gone branches" can select `clean-gone`.
- "The implementation is finished" does not authorize a Git side effect.

## `$commit`

Inspects `git status`, `git diff HEAD`, the current branch, and the latest ten commits. It stages the current changes and creates exactly one commit with:

```text
Generated with [Codex](https://chatgpt.com/codex)
Model: <active-model-slug> <active-reasoning-effort>

Co-authored-by: Codex <noreply@openai.com>
```

Codex supplies the active model slug directly, but the current hook schema does not expose reasoning effort. The plugin exactly matches the current `turn_id` and model against a `turn_context` near the end of `transcript_path`; if that fails, it uses `model_reasoning_effort` only when user config targets the same model. It extracts only attribution fields and never copies or stores prompt content. Because transcript format is not stable, failure omits the effort suffix; an untrusted hook or missing model context still stops the skill before staging or committing.

It does not push or open a PR, and it does not create an empty commit when there are no changes.

## `$commit-push-pr`

Inspects the current status, diff, and branch. It creates a new branch only when the current branch is exactly `main`, then creates one commit, pushes to `origin`, and opens a PR with `gh pr create`.

The skill requires explicit PR intent. Like the original, it has no publish-without-a-new-commit path and does not create policy-driven replacement branches for names other than `main`.

GitHub CLI must be installed and authenticated, and the repository must have an `origin` remote.

## `$clean-gone`

Uses `git branch -v` and `git worktree list` to find branches marked `[gone]`. For each candidate, it force-removes an associated non-main worktree with `git worktree remove --force`, then force-deletes the branch with `git branch -D`.

This deliberately matches the original destructive behavior: it does not fetch, verify merges, inspect worktree cleanliness, protect ignored files, or apply integration-branch rules. Review repository state before invoking it.

## Local validation

```bash
python -m py_compile plugins/commit-commands/hooks/model_context.py
'{"hook_event_name":"UserPromptSubmit","model":"gpt-5.6-sol","effort":"xhigh"}' | python plugins/commit-commands/hooks/model_context.py
python -m unittest discover -s tests
codex plugin list
```
