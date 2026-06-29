---
allowed-tools: Bash(git fetch:*), Bash(git branch:*), Bash(git worktree:*), Bash(git rev-parse:*)
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
git branch -v
```

3. List worktrees so branches attached to worktrees can be handled safely:

```bash
git worktree list
```

4. For each local branch marked `[gone]`:
   - If it has an associated worktree, remove that worktree first.
   - Delete the local branch after its worktree is gone.

## Suggested command

```bash
git branch -v | grep '\[gone\]' | sed 's/^[+* ]//' | awk '{print $1}' | while read branch; do
  echo "Processing branch: $branch"
  worktree=$(git worktree list | grep "\\[$branch\\]" | awk '{print $1}')
  if [ -n "$worktree" ] && [ "$worktree" != "$(git rev-parse --show-toplevel)" ]; then
    echo "  Removing worktree: $worktree"
    git worktree remove --force "$worktree"
  fi
  echo "  Deleting branch: $branch"
  git branch -D "$branch"
done
```

## Expected response

Report which worktrees and branches were removed. If no branches are marked `[gone]`, say that no cleanup was needed.
