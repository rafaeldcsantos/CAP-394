#!/bin/bash

large_files=$(find . -path ./.git -prune -o -type f -size +90M -print)

if [[ -n "$large_files" ]]; then
  echo "❌ The following files are larger than 90MB and will block the push:"
  echo "$large_files"
  echo "Please remove them or use Git LFS."
  exit 1
fi


# Add all changes
git add .

# Commit changes with a default message
git commit -m "Update changes"

# Push changes to the main branch
git push origin main
