# Commit Commands Plugin

[简体中文](../../docs/commit-commands/README.md) · [English](../../i18n/en/docs/commit-commands/README.md) · [繁體中文](../../i18n/zh-TW/docs/commit-commands/README.md) · [日本語](../../i18n/ja/docs/commit-commands/README.md) · [한국어](../../i18n/ko/docs/commit-commands/README.md)

Repository-aware Git workflows packaged as native Codex skills.

This plugin adapts Anthropic's `commit-commands` slash commands into three Codex skills:

```text
$commit
$commit-push-pr
$clean-gone
```

Codex can select a skill implicitly when the user clearly asks for its outcome. The `$skill-name` form remains the explicit override. Finishing implementation alone never authorizes a commit, push, pull request, or branch deletion.

## Skills

### `$commit`

Creates exactly one local commit for safe files related to the current task. It reads repository instructions, matches the existing commit style, screens secrets and artifacts, and appends:

```text
Co-authored-by: Codex <noreply@openai.com>
```

It never pushes or opens a pull request.

### `$commit-push-pr`

Reads repository branch policy, moves work to a compliant work branch when safe, validates and commits relevant changes, publishes the branch to `origin`, and opens a pull request against the required integration branch with GitHub CLI.

It is selected only for explicit pull request intent or an explicit request for the full commit-push-PR workflow. A commit-and-push-only or branch-publishing request does not authorize PR creation.

It never commits or pushes directly to a protected branch, force pushes, or silently resets, stashes, or rebases current work.

Requirements:

- Git must be installed and configured.
- GitHub CLI must be installed and authenticated.
- The repository must have an `origin` remote.

### `$clean-gone`

Prunes remote-tracking metadata, finds local branches whose upstream is `[gone]`, proves each candidate merged into an approved integration branch, checks linked worktrees with `git status --short --ignored=matching`, and uses only non-forced removal.

It treats tracked, untracked, and ignored paths as local data. Branch deletion runs only from a worktree whose `HEAD` is the exact integration ref used for the merge proof; otherwise the candidate is preserved and reported.

## Implicit invocation

Each skill includes a narrow trigger description:

- "Commit these changes" can select `commit`.
- "Push this branch and open a PR" can select `commit-push-pr`.
- "Clean merged gone branches" can select `clean-gone`.
- "The implementation is finished" does not authorize any of them.

## Relationship to the Claude plugin

The original Anthropic plugin exposes manually invoked `/commit`, `/commit-push-pr`, and `/clean_gone` slash commands. This adaptation preserves their workflow intent and strengthens their safety checks, while using Codex-native skills for implicit natural-language selection and explicit `$skill-name` invocation.
