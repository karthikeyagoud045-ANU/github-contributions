#!/usr/bin/env python3
"""
GitHub Contribution Automator
Generates random contributions to keep GitHub profile green
- Weekdays: 1-2 contributions
- Weekends: 5-7 contributions
"""

import subprocess
import random
import datetime
from pathlib import Path
import os

# Configuration
REPO_PATH = Path.home() / "github-contributions"
DAILY_LINES_MIN = 10
DAILY_LINES_MAX = 30

def get_contribution_count_for_day():
    """Determine contribution count based on day of week"""
    today = datetime.datetime.now().weekday()
    if today >= 5:  # Saturday or Sunday
        return random.randint(5, 7)
    else:  # Weekday
        return random.randint(1, 2)

def make_commit(message, lines_of_code=0):
    """Make a git commit with given message"""
    try:
        # Create or modify a file
        content_file = REPO_PATH / "activity.txt"
        
        # Add new line
        if content_file.exists():
            content = content_file.read_text()
        else:
            content = ""
        
        new_lines = [f"# {datetime.datetime.now().isoformat()}" for _ in range(lines_of_code)]
        content += "\n".join(new_lines) + f"\n# {message}\n"
        content_file.write_text(content)
        
        # Git commands
        subprocess.run(["git", "add", "."], cwd=REPO_PATH, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", message], cwd=REPO_PATH, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=REPO_PATH, check=True, capture_output=True)
        
        return True
    except Exception as e:
        print(f"Error making commit: {e}")
        return False

def main():
    # Initialize repo if needed
    if not (REPO_PATH / ".git").exists():
        REPO_PATH.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init"], cwd=REPO_PATH, check=True)
        subprocess.run(["git", "remote", "add", "origin", "https://github.com/karthikeyagoud045-ANU/github-contributions.git"], 
                      cwd=REPO_PATH)
        
        # Create initial commit
        (REPO_PATH / "README.md").write_text("# Contribution Tracker\n")
        subprocess.run(["git", "add", "."], cwd=REPO_PATH, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=REPO_PATH, check=True)
    
    # Get target contributions for today
    target = get_contribution_count_for_day()
    
    for i in range(target):
        lines = random.randint(DAILY_LINES_MIN, DAILY_LINES_MAX)
        make_commit(f"Auto contribution {i+1}/{target}", lines)
    
    print(f"Created {target} contributions for today")

if __name__ == "__main__":
    main()