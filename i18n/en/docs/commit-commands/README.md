# commit-commands

[简体中文](../../../../docs/commit-commands/README.md) · [English](README.md) · [繁體中文](../../../zh-TW/docs/commit-commands/README.md) · [日本語](../../../ja/docs/commit-commands/README.md) · [한국어](../../../ko/docs/commit-commands/README.md)

`commit-commands` packages common Git workflows as three native Codex skills:

```text
$commit
$commit-push-pr
$clean-gone
```

Codex can select a skill from explicit natural-language intent. Use `$skill-name` to force a specific skill. Finishing implementation alone never authorizes a commit, push, pull request, or branch deletion.

## Installation and enablement

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
codex plugin add commit-commands@zaunekko
```

After installing or updating, start a new Codex thread so the new skill metadata is available.

## Implicit selection examples

- "Commit these changes" can select `commit`.
- "Push this branch and open a PR" can select `commit-push-pr`.
- "Clean merged gone branches" can select `clean-gone`.
- "The implementation is finished" does not authorize a Git side effect.

## `$commit`

Reads repository policy, inspects the branch, worktree, index, and recent commit style, stages only safe files relevant to the current task, and creates one local commit.

It skips obvious credentials, private keys, environment files, dependency directories, build output, caches, logs, and machine-specific files. Generated commits include:

```text
Co-authored-by: Codex <noreply@openai.com>
```

This skill never pushes or opens a pull request.

## `$commit-push-pr`

Reads repository instructions such as `AGENTS.md` and `CONTRIBUTING.md`, then determines the required base, work branch, validation commands, and pull request target.

- It never commits or pushes directly to `main`, `master`, `dev`, `develop`, or another protected branch.
- It creates a compliant work branch only when current changes can be preserved safely.
- It never resets, stashes, rebases, force pushes, or bypasses validation on its own.
- It creates one commit, publishes the work branch, and opens a pull request with GitHub CLI.

This skill requires an installed and authenticated GitHub CLI plus an `origin` remote.

## `$clean-gone`

Runs `git fetch --prune`, then checks local branches whose upstream is `[gone]`. `[gone]` means only that the remote reference was deleted; it does not prove the local commits were merged.

A candidate is removed only when it is not current or protected, is merged into a repository-approved integration branch, has no dirty or unreadable linked worktree, and passes Git's non-forced deletion checks. Every other candidate is preserved with a reason.

## Relationship to the Claude plugin

The Anthropic original provides manually invoked slash commands. This adaptation preserves the workflow intent and strengthens its safeguards while using native Codex skills for implicit natural-language selection and explicit `$skill-name` invocation.

## Local validation

```bash
python -m unittest discover -s tests
codex plugin list
```
