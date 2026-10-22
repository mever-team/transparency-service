#!/bin/bash
set -e

# Ensure we're on eval
git switch eval

# Save the current agent_eval tree
saved_commit=$(git rev-parse HEAD)

# Merge dev without committing immediately
git merge --no-commit --no-ff dev || {
    echo "Merge has conflicts. Resolve them before continuing."
    exit 1
}

# Restore agent_eval exactly as it was before the merge
git restore --source="$saved_commit" --staged --worktree -- agent_eval/ merge-dev.sh

# Complete the merge
git commit -m "Merge dev into eval"