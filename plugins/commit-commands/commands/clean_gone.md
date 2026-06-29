---
allowed-tools: Bash(git fetch:*), Bash(git branch:*), Bash(git worktree:*), Bash(git rev-parse:*), Bash(git merge-base:*), Bash(git status:*), Bash(git -C:*)
description: Clean up local branches marked as gone
---

## Your task

Clean up stale local branches whose upstream branches have already been removed from the remote.

## Workflow

1. Refresh remote branch metadata:

```bash
git fetch --prune
```

2. List local branches and identify entries marked `[gone]`:

```bash
git branch -vv
```

3. Read repository-local workflow instructions and identify the repository's protected or integration branches, such as `main`, `master`, `dev`, or `develop`.

4. List worktrees in a machine-readable format so branches attached to worktrees can be handled safely:

```bash
git worktree list --porcelain
```

5. For each local branch marked `[gone]`:
   - Skip the current branch.
   - Verify that its tip is merged into at least one repository-approved integration branch:

     ```bash
     git merge-base --is-ancestor <branch> <approved-base>
     ```

   - If no approved base contains the branch tip, skip the branch as unmerged.
   - If it has an associated worktree, inspect that worktree first:

     ```bash
     git -C <worktree-path> status --short
     ```

   - If the worktree is dirty or cannot be inspected, skip the branch and preserve the worktree.
   - If the worktree is clean, remove it with `git worktree remove <worktree-path>`.
   - Delete the branch with `git branch -d <branch>`. If Git refuses, preserve the branch and report the reason.

## Safety rules

- A `[gone]` upstream proves only that the remote reference was deleted; it does not prove that the local work is merged.
- Never remove the main worktree, a dirty worktree, the current branch, or an unmerged branch.
- Never bypass Git's merged-branch checks during cleanup.

## Expected response

Report which worktrees and branches were removed and which candidates were skipped, including the reason. If no branches are marked `[gone]`, say that no cleanup was needed.
