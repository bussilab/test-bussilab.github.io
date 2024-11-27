#!/bin/bash

# Pull the latest changes to ensure the repo is up-to-date
git pull --rebase origin master || git rebase --abort

# Run the update script
python3 update.py _data/posts.yml

# Check for changes
if git diff --quiet; then
  echo "No changes detected. Exiting."
  exit 0
fi

# Stage, commit, and push changes
git add _data/posts.yml
git commit -m "[skip update] Automated update: $(date)"
git push origin master

