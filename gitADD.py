import subprocess
import os
import re

# ---- Config ----
repo_path = r"D:\Main\LETTCODE GITHUB"
script_name = "gitADD.py"  # This script’s filename
os.chdir(repo_path)

# ---- Folder creation config ----
max_problem_number = 4000
subfolder_size = 100
topfolder_size = 1000
num_digits = len(str(max_problem_number))

# ---- Create folders if missing ----
for top_start in range(1, max_problem_number + 1, topfolder_size):
    top_end = min(top_start + topfolder_size - 1, max_problem_number)
    top_folder_name = f"{str(top_start).zfill(num_digits)}-{str(top_end).zfill(num_digits)}"
    top_folder_path = os.path.join(repo_path, top_folder_name)
    os.makedirs(top_folder_path, exist_ok=True)

    for sub_start in range(top_start, top_end + 1, subfolder_size):
        sub_end = min(sub_start + subfolder_size - 1, top_end)
        sub_folder_name = f"{str(sub_start).zfill(num_digits)}-{str(sub_end).zfill(num_digits)}"
        sub_folder_path = os.path.join(top_folder_path, sub_folder_name)
        os.makedirs(sub_folder_path, exist_ok=True)

print("All folders created successfully!")

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

    # Pull before push
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
