import json
import os
import sys
import shutil
import re

def reorder_json_items(file_path):
    # Create a backup of the original file
    backup_path = f"{file_path}.bak"
    shutil.copyfile(file_path, backup_path)
    print(f"Backup created at: {backup_path}")

    try:
        # Load the existing JSON data with utf-8 encoding
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"Encoding error: {e}. Try a different encoding or check the file content.")
        sys.exit(1)

    # Check the number of original entries
    original_count = len(data['items'])
    print(f"Original number of entries: {original_count}")
    
    # Reorder items by title (lowercase) with special characters first
    def sort_key(item):
        title = item[1]['title']
        # Lowercase title and prioritize special characters
        return (re.sub(r'[^a-zA-Z0-9]', '', title).lower(), title.lower())

    sorted_items = dict(sorted(data['items'].items(), key=sort_key))
    
    # Update the items with sorted order
    data['items'] = sorted_items
    
    # Save the updated JSON back to the file with utf-8 encoding
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    # Check the number of new entries
    new_count = len(data['items'])
    print(f"New number of entries: {new_count}")
    
    # Ensure the counts match
    if original_count == new_count:
        print("Entry counts match. Reordering successful.")
    else:
        print("Entry counts do not match! Something went wrong.")

if __name__ == "__main__":
    # Get the JSON file path from command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python reorder_json.py <path_to_your_file.json>")
        sys.exit(1)

    json_path = sys.argv[1]
    
    # Check if the file exists
    if not os.path.isfile(json_path):
        print(f"File not found: {json_path}")
        sys.exit(1)

    reorder_json_items(json_path)
