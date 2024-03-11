#!/bin/bash

# go to the right directory
cd /home/pi/Documents/Guild-Officer-Elections-2024/src

# Pull any changes
git pull -X theirs

# Run the application
python main.py

# Add all files to git
git add --all

# Commit changes
git commit -m "Update"

# Push changes to GitHub
git push
