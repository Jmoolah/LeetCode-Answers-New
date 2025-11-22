import subprocess
import os

repo_path = r"D:\Main\LETTCODE GITHUB"
os.chdir(repo_path)

print("Syncing with remote repository...")

# Pull with rebase to sync with remote
result = subprocess.run(["git", "pull", "--rebase"], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(result.stderr)

# Check if there were conflicts
if result.returncode != 0:
    print("\n❌ Conflicts detected or pull failed!")
    print("You need to manually resolve conflicts.")
    print("\nTo resolve:")
    print("1. Open conflicted files and fix them")
    print("2. Run: git add .")
    print("3. Run: git rebase --continue")
    print("4. Run: git push")
else:
    print("\n✅ Successfully synced with remote!")
    
    # Now push
    print("\nPushing to remote...")
    push_result = subprocess.run(["git", "push"], capture_output=True, text=True)
    print(push_result.stdout)
    if push_result.stderr:
        print(push_result.stderr)
    
    if push_result.returncode == 0:
        print("\n✅ Successfully pushed to remote!")
    else:
        print("\n❌ Push failed!")