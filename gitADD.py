import subprocess
import os
import re

# Path to your local repo
repo_path = r"D:\Main\LETTCODE GITHUB"
os.chdir(repo_path)

# Get git status
status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
changes = status.stdout.strip()

if not changes:
    print("No changes detected. Nothing to commit.")
else:
    added = []
    modified = []
    removed = []

    for line in changes.splitlines():
        code, path = line[:2], line[3:]
        if code == "??":
            added.append(path)
        elif code.strip() == "M":
            modified.append(path)
        elif code.strip() == "D":
            removed.append(path)

    # Stage all changes
    subprocess.run(["git", "add", "."])

    # Build a concise commit message
    messages = []
    if added:
        messages.append("added " + ", ".join([os.path.basename(f) for f in added]))
    if modified:
        messages.append("modified " + ", ".join([os.path.basename(f) for f in modified]))
    if removed:
        messages.append("removed " + ", ".join([os.path.basename(f) for f in removed]))

    commit_message = "; ".join(messages)

    # Commit changes
    subprocess.run(["git", "commit", "-m", commit_message])

    # Push to GitHub
    subprocess.run(["git", "push"])

    print("Changes committed and pushed with message:")
    print(commit_message)
