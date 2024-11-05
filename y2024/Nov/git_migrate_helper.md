# How to migreate git commit in a special way #

Write a python script, working in a git repo, given 2 git commit hash, and calculate all changes from the first to the second, and do following task:

1. Copy all *.swift files that is created to a root folder named: "diff_created" under current folder, and keep the relative path compare to current folder where running the script.
2. Copy all new created *.png files to folder "diff_created_images", grouped by it's parent folder, that is, if two file "a" and "b" are in the same folder "c", then creat a folder named "c" under "diff_created_images" and copy "a" and "b" into it.
3. Copy any other file is not a swift file or png file into the folder "diff_created_other", with the relative path too.
4. Create a index file named "ChangeListSwift.json" under "diff_changed" folder for all changed *.swift, put each file as a json entry, and "path" property to show the relative path to current path, and "name" field for the file name, order by the path field.
5. Create a index file named "ChangeListOther.json" for other changed file name and content format same with "ChangeListSwift.json"
6. Create a index file under "diff_special" folder for all other file that is not in the list above, and give the reason, e.g. file was removed.

import os
import subprocess
import json
import shutil
from pathlib import Path

# Define directories for output
ROOT_DIR = Path.cwd()
DIFF_CREATED = ROOT_DIR / "diff_created"
DIFF_CREATED_IMAGES = ROOT_DIR / "diff_created_images"
DIFF_CREATED_OTHER = ROOT_DIR / "diff_created_other"
DIFF_CHANGED = ROOT_DIR / "diff_changed"
DIFF_SPECIAL = ROOT_DIR / "diff_special"

# Ensure output directories exist
DIFF_CREATED.mkdir(exist_ok=True)
DIFF_CREATED_IMAGES.mkdir(exist_ok=True)
DIFF_CREATED_OTHER.mkdir(exist_ok=True)
DIFF_CHANGED.mkdir(exist_ok=True)
DIFF_SPECIAL.mkdir(exist_ok=True)

def git_diff_files(hash1, hash2):
    """Get list of changed files between two commits"""
    result = subprocess.run(
        ["git", "diff", "--name-status", hash1, hash2],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise Exception("Error running git diff")
    
    files = []
    for line in result.stdout.strip().split("\n"):
        status, path = line.split("\t", 1)
        files.append((status, path))
    
    return files

def copy_file(src, dest):
    """Copy file and create necessary parent directories"""
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)

def process_files(changed_files):
    swift_files = []
    other_files = []
    special_files = []

    for status, path in changed_files:
        src_path = ROOT_DIR / path
        if status == "A":  # File was created
            if path.endswith(".swift"):
                dest_path = DIFF_CREATED / path
                copy_file(src_path, dest_path)
            elif path.endswith(".png"):
                parent_folder = DIFF_CREATED_IMAGES / src_path.parent.name
                parent_folder.mkdir(parents=True, exist_ok=True)
                dest_path = parent_folder / src_path.name
                copy_file(src_path, dest_path)
            else:
                dest_path = DIFF_CREATED_OTHER / path
                copy_file(src_path, dest_path)
        elif status == "M":  # File was modified
            if path.endswith(".swift"):
                swift_files.append({
                    "path": str(path),
                    "name": Path(path).name
                })
            else:
                other_files.append({
                    "path": str(path),
                    "name": Path(path).name
                })
        else:
            # File was deleted, renamed, etc.
            special_files.append({
                "path": str(path),
                "reason": "File was removed" if status == "D" else "File had special status"
            })

    return swift_files, other_files, special_files

def save_json(data, filepath):
    """Save list of dictionaries to a JSON file"""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def main(hash1, hash2):
    # Step 1: Get list of files changed between the two commits
    changed_files = git_diff_files(hash1, hash2)
    
    # Step 2: Process files into categories
    swift_files, other_files, special_files = process_files(changed_files)
    
    # Step 3: Save index files
    if swift_files:
        save_json(sorted(swift_files, key=lambda x: x["path"]), DIFF_CHANGED / "ChangeListSwift.json")
    if other_files:
        save_json(sorted(other_files, key=lambda x: x["path"]), DIFF_CHANGED / "ChangeListOther.json")
    if special_files:
        save_json(special_files, DIFF_SPECIAL / "SpecialFileList.json")

if __name__ == "__main__":
    # Replace 'hash1' and 'hash2' with actual commit hashes
    commit_hash1 = input("Enter the first commit hash: ").strip()
    commit_hash2 = input("Enter the second commit hash: ").strip()
    main(commit_hash1, commit_hash2)
