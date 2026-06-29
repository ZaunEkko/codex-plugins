---
name: clean-gone
description: Safely clean local Git branches whose upstream is marked gone, only when merged into an approved integration branch and associated worktrees are clean. Use when the user explicitly asks to clean stale, gone, or deleted-remote branches, or remove obsolete worktrees. Never use merely because stale branches exist.
---

# Clean Gone Branches

Remove only stale local branches that can be proven merged and safe to delete.

## Workflow

1. Read repository instructions and identify protected branches and approved integration branches such as `main`, `master`, `dev`, or `develop`.
2. Run `git fetch --prune` to refresh remote-tracking metadata.
3. Inspect `git branch -vv` and collect only local branches whose upstream is marked `[gone]`.
4. Inspect `git worktree list --porcelain` and map every candidate branch to its associated worktree, if any.
5. For each candidate:
   - Skip the current branch and every protected or integration branch.
   - Verify its tip is an ancestor of at least one approved local or remote integration branch with `git merge-base --is-ancestor`.
   - If no approved base contains the tip, preserve the branch as unmerged.
   - If it has a linked worktree, inspect that worktree with `git -C <path> status --short`.
   - Preserve the branch and worktree if the worktree is dirty, is the main worktree, or cannot be inspected.
   - Remove a verified clean linked worktree with non-forced `git worktree remove <path>`.
   - Delete the verified merged branch with non-forced `git branch -d <branch>`.
6. Report every removed worktree and branch, plus every skipped candidate and its reason. If no candidates exist, report that no cleanup was needed.

## Safety rules

- `[gone]` proves only that the upstream reference was deleted; it does not prove that local commits were merged.
- Never remove the main worktree, a dirty or unreadable worktree, the current branch, a protected branch, or an unmerged branch.
- Never use `git branch -D`, `git worktree remove --force`, or another force option.
- Do not delete remote branches or perform unrelated work.
