import subprocess
import os
from datetime import datetime

# Path to your local repo
repo_path = r"D:\Main\LETTCODE GITHUB"

# Go to repo
os.chdir(repo_path)

# 1️⃣ Check Git status
status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
changes = status.stdout.strip()

if not changes:
    print("No changes detected. Nothing to commit.")
else:
    print("Changes detected:")
    print(changes)
    
    # 2️⃣ Stage all changes
    subprocess.run(["git", "add", "."])
    
    # 3️⃣ Create a smart commit message
    # We'll list changed files in the message
    changed_files = [line[3:] for line in changes.splitlines()]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Auto-update {', '.join(changed_files)} @ {timestamp}"
    
    # 4️⃣ Commit changes
    subprocess.run(["git", "commit", "-m", commit_message])
    
    # 5️⃣ Push to GitHub
    subprocess.run(["git", "push"])
    
    print("Changes committed and pushed with message:")
    print(commit_message)
