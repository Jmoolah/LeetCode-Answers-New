import os

# Current folder is the local repo
repo_path = os.getcwd()

max_problem_number = 4000
subfolder_size = 100
topfolder_size = 1000

# Number of digits for padding
num_digits = len(str(max_problem_number))

for top_start in range(1, max_problem_number + 1, topfolder_size):
    top_end = min(top_start + topfolder_size - 1, max_problem_number)
    top_folder_name = f"{str(top_start).zfill(num_digits)}-{str(top_end).zfill(num_digits)}"
    top_folder_path = os.path.join(repo_path, top_folder_name)
    os.makedirs(top_folder_path, exist_ok=True)

    # Create subfolders of 100 inside each top-level folder
    for sub_start in range(top_start, top_end + 1, subfolder_size):
        sub_end = min(sub_start + subfolder_size - 1, top_end)
        sub_folder_name = f"{str(sub_start).zfill(num_digits)}-{str(sub_end).zfill(num_digits)}"
        sub_folder_path = os.path.join(top_folder_path, sub_folder_name)
        os.makedirs(sub_folder_path, exist_ok=True)

print("All folders created successfully!")
