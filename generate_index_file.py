import os
import re
import shutil
from datetime import datetime

def extract_title(file_path):
    # Read the first line in the file to get the title
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            title_match = re.match(r'# (.+) #', line.strip())
            if title_match:
                return title_match.group(1)
    return "Untitled"  # Default title if no match found

def get_month_name(date):
    # Convert a date to the corresponding month abbreviation (e.g., "Jan" for January)
    return date.strftime('%b')

def move_file_to_month_folder(file_path, year_path):
    # Get file's modification date
    file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    month_name = get_month_name(file_mod_time)
    
    # Create month folder if it doesn't exist
    month_folder_path = os.path.join(year_path, month_name)
    if not os.path.exists(month_folder_path):
        os.makedirs(month_folder_path)
    
    # Move file to the month folder
    new_file_path = os.path.join(month_folder_path, os.path.basename(file_path))
    shutil.move(file_path, new_file_path)
    return new_file_path

def generate_index(folder_path):
    index_content = "# FunnyStories\nAnything interesting!\n\n"
    year_pattern = re.compile(r'\d{4}')  # Matches any 4-digit year within the folder name
    month_pattern = re.compile(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)$', re.IGNORECASE)
    exclude_pattern = re.compile(r'(temp|working|personal)', re.IGNORECASE)

    # Loop through each directory in the given folder
    for year_folder in sorted(os.listdir(folder_path)):
        year_path = os.path.join(folder_path, year_folder)
        
        # Only process directories that contain a 4-digit year and do not contain excluded keywords
        if (
            os.path.isdir(year_path)
            and year_pattern.search(year_folder)
            and not exclude_pattern.search(year_folder)
        ):
            # Move any loose .md files in the year folder to the appropriate month folder
            for item in os.listdir(year_path):
                item_path = os.path.join(year_path, item)
                if os.path.isfile(item_path) and item_path.endswith('.md'):
                    item_path = move_file_to_month_folder(item_path, year_path)

            # Loop through each monthly subdirectory
            for month_folder in sorted(os.listdir(year_path)):
                month_path = os.path.join(year_path, month_folder)
                
                # Only process directories that match month names
                if os.path.isdir(month_path) and month_pattern.match(month_folder):
                    # Generate "YYYY-MM" header for the month
                    month_num = datetime.strptime(month_folder, "%b").month
                    month_section = f"{year_folder}-{month_num:02d}"
                    index_content += f"## {month_section} ##\n"
                    
                    # List each .md file within the month folder
                    for md_file in sorted(os.listdir(month_path)):
                        if md_file.endswith('.md'):
                            md_file_path = os.path.join(month_path, md_file)
                            title = extract_title(md_file_path)
                            relative_path = os.path.relpath(md_file_path, folder_path)
                            index_content += f"* [{title}]({relative_path})\n"
                    index_content += "\n"  # Blank line between months

    # Write the generated index content to README.md
    readme_path = os.path.join(folder_path, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as readme_file:
        readme_file.write(index_content)

    print(f"README.md generated successfully at {readme_path}")

# Replace '/path/to/your/folder' with the actual folder path
generate_index('./')
