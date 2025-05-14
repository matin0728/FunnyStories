# Caculate header files dependencies #

> Write a python script to caculate header file dependencies, given source files, base folder, destination folder as params, follow rules:
>  1. Give one or more header file as source files.
>  2. If the file import another header file, copy that file to destination folder, keep the relative path and create folders if needed.
>  3. Caculate dependencies recursively.
>  4. The path that a header file imported from can be a relative path base on the base path or base on the path where it is imported.
>  5. The path should allows common chars that MacOS allows, such as digits.

Here's a Python script that calculates header file dependencies and copies the necessary files to the destination folder while preserving the relative paths. It supports recursive dependency resolution and handles both base-path-relative and import-path-relative includes.

Here’s the Python script:

```python
import os
import shutil
import re

def parse_includes(file_path):
    """Extracts the included header files from a source file."""
    include_pattern = re.compile(r'#include\s+"([^"]+)"')
    includes = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = include_pattern.search(line)
            if match:
                includes.append(match.group(1))
    return includes

def copy_file_with_folders(src, dst):
    """Copies a file to the destination path, creating necessary folders."""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)

def resolve_dependencies(file_path, base_path, dest_path, visited):
    """Recursively resolve and copy dependencies for a header file."""
    if file_path in visited:
        return

    visited.add(file_path)

    includes = parse_includes(file_path)
    for include in includes:
        # Resolve paths relative to the base path or the file path.
        include_path = os.path.normpath(
            os.path.join(os.path.dirname(file_path), include)
        )
        if not os.path.isabs(include_path):
            include_path = os.path.normpath(os.path.join(base_path, include))

        # Ensure the file exists before attempting to copy.
        if os.path.isfile(include_path):
            relative_path = os.path.relpath(include_path, base_path)
            dest_file_path = os.path.join(dest_path, relative_path)
            copy_file_with_folders(include_path, dest_file_path)

            # Recursively resolve dependencies for the included file.
            resolve_dependencies(include_path, base_path, dest_path, visited)

def calculate_dependencies(source_files, base_folder, destination_folder):
    """Calculate and copy header file dependencies for given source files."""
    visited = set()
    for source_file in source_files:
        full_source_path = os.path.join(base_folder, source_file)
        if os.path.isfile(full_source_path):
            resolve_dependencies(full_source_path, base_folder, destination_folder, visited)
        else:
            print(f"Warning: File '{full_source_path}' does not exist.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Calculate header file dependencies.")
    parser.add_argument("source_files", nargs='+', help="List of source header files.")
    parser.add_argument("base_folder", help="Base folder containing the source files.")
    parser.add_argument("destination_folder", help="Destination folder for copied dependencies.")

    args = parser.parse_args()

    calculate_dependencies(args.source_files, args.base_folder, args.destination_folder)
```

### Features:
1. **Dependency Parsing**: It identifies `#include` directives in the source files.
2. **Relative Path Handling**: Resolves paths relative to the base path or the file path.
3. **Recursive Resolution**: Tracks visited files to avoid processing duplicates.
4. **Folder Creation**: Ensures the folder structure is mirrored in the destination.

### Usage:
Run the script from the command line with arguments:

```bash
python script_name.py header1.h header2.h /path/to/base /path/to/destination
```

Replace `script_name.py` with the filename of the script. The script will copy all dependencies to the destination folder while preserving the folder structure.
