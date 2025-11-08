import subprocess
import os
import re

# Path to your local repo
repo_path = r"D:\Main\LETTCODE GITHUB"
script_name = "git.py"  # Change if your script has a different name
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

    # Keep track if the script itself changed
    script_changed = False

    for line in changes.splitlines():
        code, path = line[:2], line[3:]
        base_name = os.path.basename(path)

        # Detect if the script itself changed
        if base_name == script_name:
            script_changed = True
            continue  # Skip adding it to normal commit messages

        # Extract problem number from filename
        match = re.match(r"(\d+)_", base_name)
        prob_num = match.group(1) if match else None

        if code == "??":
            added.append(f"problem {prob_num}" if prob_num else base_name)
        elif code.strip() == "M":
            modified.append(f"problem {prob_num}" if prob_num else base_name)
        elif code.strip() == "D":
            removed.append(f"problem {prob_num}" if prob_num else base_name)

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

    # Append script change as a separate note if it changed
    if script_changed:
        messages.append("modified the script")

    commit_message = "; ".join(messages) if messages else "Updated repo"

    # Commit changes
    subprocess.run(["git", "commit", "-m", commit_message])

    # Push to GitHub
    subprocess.run(["git", "push"])

    print("Changes committed and pushed with message:")
    print(commit_message)
