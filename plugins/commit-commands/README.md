# Commit Commands Plugin

Streamline everyday git workflows in Codex with slash commands for committing, publishing pull requests, and cleaning up stale local branches.

This is a Codex adaptation of Anthropic's `commit-commands` plugin. It keeps the same core workflow shape while using Codex attribution:

```text
Co-authored-by: Codex <noreply@openai.com>
```

## Commands

### `/commit`

Creates one git commit with an automatically generated commit message based on staged and unstaged changes.

What it does:

1. Analyzes current git status.
2. Reviews staged and unstaged changes.
3. Checks recent commit messages to match the repository style.
4. Stages relevant safe files.
5. Creates one commit.
6. Appends Codex co-author attribution.

Usage:

```text
/commit
```

### `/commit-push-pr`

Completes a branch-to-PR workflow.

What it does:

1. Creates a new feature branch if currently on `main` or `master`.
2. Stages and commits relevant safe changes.
3. Publishes the branch to `origin`.
4. Opens a pull request with the GitHub CLI.
5. Adds a concise PR body with summary, test plan, notes/risks, and Codex attribution.

Usage:

```text
/commit-push-pr
```

Requirements:

- Git must be installed and configured.
- GitHub CLI must be installed and authenticated.
- The repository should have an `origin` remote.

### `/clean_gone`

Cleans up local branches whose upstream branches were removed from the remote.

What it does:

1. Runs a prune fetch.
2. Lists local branches with `[gone]` status.
3. Removes associated worktrees when needed.
4. Deletes stale local branches.

Usage:

```text
/clean_gone
```

## Guardrails

The commands instruct Codex to skip local-only files, generated output, dependency folders, caches, logs, and environment/config files that do not belong in the repository.

Always review the resulting commit or PR before merging.

## Attribution

Generated commits should include:

```text
Co-authored-by: Codex <noreply@openai.com>
```

This email was chosen because `openai/codex` uses `noreply@openai.com` for Codex git baseline commits.

## Relationship to Claude plugin

This plugin intentionally mirrors the public Anthropic commit commands workflow:

- `/commit`
- `/commit-push-pr`
- `/clean_gone`

The command behavior is adapted for Codex and this repository's `.codex-plugin` packaging format.
