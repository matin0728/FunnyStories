# Batch find images in assets folder #

> Write a python script, read folder name from a source file, each for one line, given a root folder, > search all its subfolder for every folder name plus a suffix ".imageset" in the source file, if 
> found, copy the first png file from the folder to a output folder, and record the folder name and 
> the png file name into a result.json file.


Here’s a Python script that reads folder names from a source file, searches for folders with the specified names plus the suffix `.imageset` within a given root directory, copies the first `.png` file from each found folder to an output directory, and records the folder name and copied file name in `result.json`.

```python
import os
import json
import shutil

def find_and_copy_images(root_folder, source_file, output_folder):
    # Read folder names from the source file
    with open(source_file, 'r') as file:
        folder_names = [line.strip() for line in file if line.strip()]
    
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Dictionary to store results for JSON output
    results = {}

    # Traverse through the root folder to search for folders matching the target names with ".imageset" suffix
    for folder_name in folder_names:
        target_folder_name = f"{folder_name}.imageset"
        found = False

        for dirpath, dirnames, _ in os.walk(root_folder):
            if target_folder_name in dirnames:
                imageset_folder = os.path.join(dirpath, target_folder_name)
                png_files = [f for f in os.listdir(imageset_folder) if f.endswith('.png')]
                
                if png_files:
                    # Copy the first PNG file found
                    first_png = png_files[0]
                    src_path = os.path.join(imageset_folder, first_png)
                    dest_path = os.path.join(output_folder, first_png)
                    shutil.copy2(src_path, dest_path)
                    
                    # Record in results
                    results[folder_name] = first_png
                    found = True
                    break
        
        if not found:
            print(f"Folder '{target_folder_name}' not found in root folder")

    # Write results to JSON file
    with open('result.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)

    print("Processing complete. Check result.json for details.")

# Parameters
root_folder = "path/to/root_folder"       # Replace with the actual root folder path
source_file = "path/to/source_file.txt"   # Replace with the actual source file path
output_folder = "path/to/output_folder"   # Replace with the actual output folder path

# Run the function
find_and_copy_images(root_folder, source_file, output_folder)
```

### Explanation of the Script

1. **Read Folder Names**: Reads each line from the `source_file`, stripping any extra whitespace.
2. **Set Up Output Folder**: Creates the output directory if it doesn’t already exist.
3. **Traverse Directory Structure**: Walks through the `root_folder` and searches for folders matching each name from the source file with the `.imageset` suffix.
4. **Copy PNG File**: If a `.imageset` folder is found and contains `.png` files, the first `.png` file is copied to the `output_folder`.
5. **Store Results**: Adds an entry to the `results` dictionary with the folder name and the copied PNG file name.
6. **Save Results to JSON**: Writes the `results` dictionary to `result.json` for easy reference.

Replace `"path/to/root_folder"`, `"path/to/source_file.txt"`, and `"path/to/output_folder"` with the actual paths as required.