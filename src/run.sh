#!/bin/bash

# go to the right directory
cd ~/Guild-Officer-Elections-2024/src

# Pull any changes
git fetch --all

# Reset the local repository to match the remote repository
git reset --hard origin/main

# Run the application
python main.py

# Add all files to git
git add --all

# Commit changes
git commit -m "Update"

# Push changes to GitHub
git push
