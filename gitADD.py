import subprocess
import os
import re
import sys

repo_path = r"D:\Main\LETTCODE GITHUB"
script_name = "gitADD.py"

os.chdir(repo_path)

# -------------------------------------------------
# AUTO-MOVE LOOSE SOLUTION FILES INTO RANGE FOLDERS
# -------------------------------------------------
for item in os.listdir(repo_path):
    full_path = os.path.join(repo_path, item)

    # Skip directories and git/scripts
    if os.path.isdir(full_path):
        continue
    if item in {script_name, "git.py", "git_sync.py"}:
        continue

    match = re.match(r"(\d+)_", item)
    if not match:
        continue

    prob_num = int(match.group(1))

    # Determine 1000-range
    thousand_start = ((prob_num - 1) // 1000) * 1000 + 1
    thousand_end = thousand_start + 999
    thousand_folder = f"{thousand_start:04d}-{thousand_end:04d}"

    # Determine 100-range
    hundred_start = ((prob_num - 1) // 100) * 100 + 1
    hundred_end = hundred_start + 99
    hundred_folder = f"{hundred_start:04d}-{hundred_end:04d}"

    target_dir = os.path.join(repo_path, thousand_folder, hundred_folder)
    os.makedirs(target_dir, exist_ok=True)

    new_path = os.path.join(target_dir, item)

    if not os.path.exists(new_path):
        print(f"Moving {item} → {thousand_folder}/{hundred_folder}/")
        os.rename(full_path, new_path)

# -------------------------------------------------
# GIT PULL
# -------------------------------------------------
print("\nPulling latest changes...")
pull = subprocess.run(
    ["git", "pull", "origin", "main"],
    capture_output=True,
    text=True
)

print(pull.stdout)
if pull.returncode != 0:
    print("Pull failed:")
    print(pull.stderr)
    sys.exit(1)

# -------------------------------------------------
# GIT STATUS
# -------------------------------------------------
status = subprocess.run(
    ["git", "status", "--porcelain"],
    capture_output=True,
    text=True
)

changes = status.stdout.strip()

if not changes:
    print("No changes detected.")
    sys.exit(0)

added, modified, removed = set(), set(), set()
script_changed = False

for line in changes.splitlines():
    code = line[:2]
    path = line[3:]
    base = os.path.basename(path)

    if base == script_name:
        script_changed = True
        continue

    match = re.search(r"(\d{4})-(\d{4})", path)
    label = match.group(0) if match else base

    if code == "??":
        added.add(label)
    elif code.strip() == "M":
        modified.add(label)
    elif code.strip() == "D":
        removed.add(label)

# -------------------------------------------------
# STAGE & COMMIT SOLUTION FILES
# -------------------------------------------------
subprocess.run(["git", "add", "."])

if script_changed:
    subprocess.run(["git", "reset", script_name])

messages = []
if added:
    messages.append("added " + ", ".join(sorted(added)))
if modified:
    messages.append("modified " + ", ".join(sorted(modified)))
if removed:
    messages.append("removed " + ", ".join(sorted(removed)))

if messages:
    commit_msg = "; ".join(messages)
    subprocess.run(["git", "commit", "-m", commit_msg])
    subprocess.run(["git", "push"])
    print("\nCommitted:")
    print(commit_msg)

# -------------------------------------------------
# COMMIT SCRIPT SEPARATELY
# -------------------------------------------------
if script_changed:
    subprocess.run(["git", "add", script_name])
    subprocess.run(["git", "commit", "-m", "updated gitADD automation"])
    subprocess.run(["git", "push"])
    print("Script committed separately.")
