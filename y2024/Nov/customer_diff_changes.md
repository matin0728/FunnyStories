# Create customer diff changes #

```
Write a python script to modify file contents, follow instructions bellow:

1. Given a "source" folder path and "target" folder path, and a path for a list json file to the script file as parameters.
2. For every entry in the json file, there is a Swift file can be found with the "path" relative to source folder, if target file exits in source folder, find another file named in the "target" folder or its subfolders, the name can be the same or has an extra prefix like "FXH_", find all names used as class name in the target Swift file, these names may has or not has a prefix "FXH_", rename all class names in the source file, keep the same pattern that they are using in the target file, then replace the contents of target file using the result.
3. The class name used in the target file could be indentified though following pattern: "class ClassName", ": ClassName {", "ClassName.self", " ClassName(", "[ClassName]", ": ClassName)", "= ClassName(", "extension ClassName:"
4. If a class name is renamed, record a unque record in "result.md", given the old name and the replaced.

```

To create this script, we'll need to do the following:

1. **Read the JSON File**: Load the list of Swift files and their paths.
2. **Locate the Target Files**: For each Swift file in the JSON list, locate the corresponding file in the target folder with the same or prefixed name.
3. **Extract Class Names**: Identify and map class names in the target file, handling prefixes as specified.
4. **Rename Classes in Source Files**: Based on the target file's class names, rename the classes in the source file, preserving prefixes.
5. **Write Changes to Target File**: Replace the content in the target file with the modified source content.
6. **Log Changes**: Write each renaming instance to `result.md`.

Here’s a Python script to accomplish this:

```python
import os
import json
import re
from pathlib import Path

def load_json(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

def find_matching_target_file(source_file, target_folder):
    # Check if there's an exact match with prefix "FXH_" or no prefix
    possible_names = [source_file.name, f"FXH_{source_file.name}"]
    for root, _, files in os.walk(target_folder):
        for file in files:
            if file in possible_names:
                return Path(root) / file
    return None

def extract_class_names(file_path):
    class_pattern = re.compile(r'\bclass\s+(\w+)|:\s+(\w+)\s*\{|\b(\w+)\.self|\[\s*(\w+)\s*\]|\b(\w+)\(')
    class_names = set()

    with open(file_path, 'r') as f:
        content = f.read()
        matches = class_pattern.findall(content)
        class_names.update(filter(None, [name for match in matches for name in match]))
    
    return class_names

def rename_classes(content, class_map):
    # Replace all occurrences of each class name in the content according to the class_map
    for old_name, new_name in class_map.items():
        # Update all patterns that match "class ClassName", ": ClassName {", "ClassName.self", " ClassName(", "[ClassName]", ": ClassName)"
        patterns = [
            rf'\bclass\s+{old_name}\b',
            rf':\s+{old_name}\s+\{{',
            rf'\b{old_name}\.self\b',
            rf'\[{old_name}\]',
            rf':\b{old_name}\(',
        ]
        for pattern in patterns:
            content = re.sub(pattern, lambda m: m.group().replace(old_name, new_name), content)
    return content

def update_file(source_file, target_file, result_log):
    source_class_names = extract_class_names(source_file)
    target_class_names = extract_class_names(target_file)
    
    # Create a map of class names to rename in source file based on target file names
    class_map = {}
    for source_name in source_class_names:
        for target_name in target_class_names:
            if source_name.lstrip("FXH_") == target_name.lstrip("FXH_"):
                class_map[source_name] = target_name
                result_log.append(f"{source_name} -> {target_name}")
                break

    # Rename classes in source file content
    with open(source_file, 'r') as f:
        source_content = f.read()
    modified_content = rename_classes(source_content, class_map)

    # Write the modified content back to the target file
    with open(target_file, 'w') as f:
        f.write(modified_content)

def main(source_folder, target_folder, json_path):
    data = load_json(json_path)
    result_log = []

    for entry in data:
        relative_path = entry['path']
        source_file = Path(source_folder) / relative_path
        if source_file.exists():
            target_file = find_matching_target_file(source_file, target_folder)
            if target_file:
                update_file(source_file, target_file, result_log)
    
    # Write changes log to result.md
    with open('result.md', 'w') as f:
        f.write("\n".join(result_log))

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print("Usage: python script.py <source_folder> <target_folder> <json_path>")
    else:
        source_folder = sys.argv[1]
        target_folder = sys.argv[2]
        json_path = sys.argv[3]
        main(source_folder, target_folder, json_path)
```

### Explanation

- **Regex Patterns**: We use regular expressions to locate class names based on the patterns specified in the instructions.
- **Class Mapping**: We create a mapping between source class names and target class names, preserving prefixes where possible.
- **Updating Target Files**: The script modifies the content of the target file by replacing each class name in the source content based on the mapping.
- **Logging**: Any renaming is recorded in `result.md`.

### Usage

Run the script with:
```sh
python script.py <source_folder> <target_folder> <json_path>
```

### Note
This script assumes:
- Class names in the source and target are mostly similar with or without a prefix.
- Target files may have different names but can be identified by matching the original filename with an optional prefix. 

This should address the renaming and logging requirements! Let me know if you'd like adjustments.