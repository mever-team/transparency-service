set -e  # stop on first error

# Ensure clean working tree
if ! git diff-index --quiet HEAD --; then
  echo "Working tree is dirty. Commit or stash first."
  exit 1
fi

echo "Updating dev..."
git checkout dev
git pull --ff-only

echo "Updating deploy..."
git checkout deploy
git merge dev
git push origin deploy

echo "Returning to dev..."
git checkout dev

echo "Done ✅"
