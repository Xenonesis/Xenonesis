#!/bin/bash

# GitHub Statistics Auto-Update Script
# Runs the Python updater and commits changes

set -e

echo "🚀 Starting GitHub Statistics Update Process..."

# Check if Python script exists
if [ ! -f "scripts/update-github-stats.py" ]; then
    echo "❌ Error: update-github-stats.py not found!"
    exit 1
fi

# Install required Python packages
echo "📦 Installing required packages..."
pip install -q requests python-dotenv

# Run the statistics update
echo "📊 Updating GitHub statistics..."
python scripts/update-github-stats.py

# Check if there are changes to commit
if git diff --quiet; then
    echo "✅ No changes detected. Statistics are up to date."
else
    echo "📝 Changes detected. Committing updates..."
    
    # Configure git if needed
    git config --global user.name "${GITHUB_ACTOR:-github-actions[bot]}"
    git config --global user.email "${GITHUB_ACTOR:-github-actions[bot]}@users.noreply.github.com"
    
    # Add and commit changes
    git add README.md repository-analytics-auto.md
    git commit -m "🤖 Auto-update GitHub statistics - $(date '+%Y-%m-%d %H:%M:%S')"
    
    # Push changes
    git push
    
    echo "✅ Statistics updated and committed successfully!"
fi

echo "🎉 GitHub Statistics Update Process Complete!"