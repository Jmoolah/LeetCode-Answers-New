import subprocess
import os
import re
import shutil

repo_path = r"D:\Main\LETTCODE GITHUB"
script_name = "gitADD.py"  # Your script filename
os.chdir(repo_path)

# Define folder ranges
def get_folder_for_problem(prob_num):
    """Returns the folder name for a given problem number"""
    num = int(prob_num)
    if num <= 1000:
        return "1-1000"
    elif num <= 2000:
        return "1001-2000"
    elif num <= 3000:
        return "2001-3000"
    elif num <= 4000:
        return "3001-4000"
    else:
        # For problems beyond 4000, create folders in increments of 1000
        start = ((num - 1) // 1000) * 1000 + 1
        end = start + 999
        return f"{start}-{end}"

# Create folders if they don't exist
folders = ["1-1000", "1001-2000", "2001-3000", "3001-4000"]
for folder in folders:
    os.makedirs(folder, exist_ok=True)

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

        # Organize file into correct folder if it's a new/modified problem file
        if prob_num and code in ["??", "M ", " M"]:
            target_folder = get_folder_for_problem(prob_num)
            target_path = os.path.join(target_folder, base_name)
            
            # Only move if it's not already in the correct location
            if path != target_path and os.path.exists(path):
                os.makedirs(target_folder, exist_ok=True)
                shutil.move(path, target_path)
                print(f"Moved {base_name} to {target_folder}/")

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