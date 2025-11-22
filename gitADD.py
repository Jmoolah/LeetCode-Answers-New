import subprocess
import os
import re

repo_path = r"D:\Main\LETTCODE GITHUB"
script_name = "gitADD.py"  # Your script filename
os.chdir(repo_path)

# Pull latest changes from remote
print("Pulling latest changes from remote...")
pull_result = subprocess.run(["git", "pull", "origin", "main"], capture_output=True, text=True)
print(pull_result.stdout)
if pull_result.returncode != 0:
    print("Error during pull:")
    print(pull_result.stderr)
    exit(1)

# Get git status
status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
changes = status.stdout.strip()

if not changes:
    print("No changes detected. Nothing to commit.")
else:
    added = []
    modified = []
    removed = []
    script_changed = False

    for line in changes.splitlines():
        code, path = line[:2], line[3:]
        base_name = os.path.basename(path)

        if base_name == script_name:
            script_changed = True
            continue

        match = re.match(r"(\d+)_", base_name)
        prob_num = match.group(1) if match else None

        if code == "??":
            added.append(f"problem {prob_num}" if prob_num else base_name)
        elif code.strip() == "M":
            modified.append(f"problem {prob_num}" if prob_num else base_name)
        elif code.strip() == "D":
            removed.append(f"problem {prob_num}" if prob_num else base_name)

    # Stage everything first
    subprocess.run(["git", "add", "."])
    
    # Unstage the script if it changed
    if script_changed:
        subprocess.run(["git", "reset", script_name])

    # Commit solution files
    messages = []
    if added:
        messages.append("added " + ", ".join(added))
    if modified:
        messages.append("modified " + ", ".join(modified))
    if removed:
        messages.append("removed " + ", ".join(removed))

    if messages:
        commit_message = "; ".join(messages)
        subprocess.run(["git", "commit", "-m", commit_message])
        subprocess.run(["git", "push"])
        print("Solution files committed and pushed with message:")
        print(commit_message)
    else:
        print("No solution file changes to commit.")

    # Commit script separately if it changed
    if script_changed:
        subprocess.run(["git", "add", script_name])
        subprocess.run(["git", "commit", "-m", "modified the script"])
        subprocess.run(["git", "push"])
        print("Script committed and pushed with message: modified the script")