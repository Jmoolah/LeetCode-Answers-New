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

    for line in changes.splitlines():
        code, path = line[:2], line[3:]
        base_name = os.path.basename(path)

        # Handle the script file separately
        if base_name == script_name:
            if code == "??":
                added.append("the script")
            elif code.strip() == "M":
                modified.append("the script")
            elif code.strip() == "D":
                removed.append("the script")
            continue

        # Extract problem number from filename
        match = re.match(r"(\d+)_", base_name)
        prob_num = match.group(1) if match else None

        if code == "??":
            added.append(f"problem {prob_num}" if prob_num else f"added {base_name}")
        elif code.strip() == "M":
            modified.append(f"problem {prob_num}" if prob_num else f"modified {base_name}")
        elif code.strip() == "D":
            removed.append(f"problem {prob_num}" if prob_num else f"removed {base_name}")

    # Stage all changes
    subprocess.run(["git", "add", "."])

    # Build commit message
    messages = []
    if added:
        messages.append("added " + ", ".join(added))
    if modified:
        messages.append("modified " + ", ".join(modified))
    if removed:
        messages.append("removed " + ", ".join(removed))

    commit_message = "; ".join(messages) if messages else "Updated repo"

    # Commit changes
    subprocess.run(["git", "commit", "-m", commit_message])

    # Push to GitHub
    subprocess.run(["git", "push"])

    print("Changes committed and pushed with message:")
    print(commit_message)
