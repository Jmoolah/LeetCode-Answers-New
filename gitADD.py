import subprocess
import os
import re

repo_path = r"D:\Main\LETTCODE GITHUB"
script_name = "gitADD.py"  # This script’s filename
os.chdir(repo_path)

# ---- Helper: run commands ----
def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

# ---- Get git status ----
status = run(["git", "status", "--porcelain"])
changes = status.stdout.strip()

if not changes:
    print("No changes detected. Nothing to commit.")
    exit()

added = []
modified = []
removed = []
script_changed = False

# ---- Parse changes ----
for line in changes.splitlines():
    code, path = line[:2], line[3:]
    base_name = os.path.basename(path)

    # Skip committing the script itself
    if base_name == script_name:
        script_changed = True
        continue

    # Extract problem number
    match = re.match(r"(\d+)_", base_name)
    prob_num = match.group(1) if match else None

    label = f"problem {prob_num}" if prob_num else base_name

    if code == "??":
        added.append(label)
    elif code.strip() == "M":
        modified.append(label)
    elif code.strip() == "D":
        removed.append(label)

# ---- Stage everything ----
run(["git", "add", "."])

# Unstage script if modified
if script_changed:
    run(["git", "reset", script_name])

# Build commit message
messages = []
if added:
    messages.append("added " + ", ".join(added))
if modified:
    messages.append("modified " + ", ".join(modified))
if removed:
    messages.append("removed " + ", ".join(removed))

# ---- Commit + pull + push the solution files ----
if messages:
    commit_message = "; ".join(messages)
    run(["git", "commit", "-m", commit_message])

    # IMPORTANT: pull before push
    run(["git", "pull", "--rebase"])

    run(["git", "push"])
    print("Solution files committed and pushed with message:")
    print(commit_message)
else:
    print("No solution file changes to commit.")

# ---- Commit the script separately ----
if script_changed:
    run(["git", "add", script_name])
    run(["git", "commit", "-m", "modified the script"])

    # pull before push
    run(["git", "pull", "--rebase"])

    run(["git", "push"])
    print("Script committed and pushed with message: modified the script")
