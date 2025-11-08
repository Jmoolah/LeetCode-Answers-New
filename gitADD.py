import subprocess
import os
import re

# Path to your local repo
repo_path = r"D:\Main\LETTCODE GITHUB"
script_name = "git.py"  # Name of this script
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
    script_changes = []

    for line in changes.splitlines():
        code, path = line[:2], line[3:]
        base_name = os.path.basename(path)
        
        # Separate script changes
        if base_name == script_name:
            script_changes.append((code, base_name))
            continue

        # Extract problem number from filename
        match = re.match(r"(\d+)_", base_name)
        prob_num = match.group(1) if match else "unknown"

        if code == "??":
            added.append(prob_num)
        elif code.strip() == "M":
            modified.append(prob_num)
        elif code.strip() == "D":
            removed.append(prob_num)

    # Stage all changes
    subprocess.run(["git", "add", "."])

    # Build commit message for solutions
    messages = []
    if added:
        messages.append("added problem " + ", ".join(added))
    if modified:
        messages.append("modified problem " + ", ".join(modified))
    if removed:
        messages.append("removed problem " + ", ".join(removed))

    commit_message = "; ".join(messages) if messages else "Updated repo"

    # If the script itself changed, append a note
    if script_changes:
        commit_message += "; script changed"

    # Commit changes
    subprocess.run(["git", "commit", "-m", commit_message])

    # Push to GitHub
    subprocess.run(["git", "push"])

    print("Changes committed and pushed with message:")
    print(commit_message)
