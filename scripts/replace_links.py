#!/usr/bin/env python3
import os
import json
import sys

def get_link_map_from_api():
    """
    Get JSON string from the JSON file at json_filepath, parse it, 
    and convert the array of objects into a dictionary.
    """
    try:
        with open("links_data.json", 'r', encoding='utf-8') as f:
            json_string = f.read()
    except Exception as e:
        print(f"Error: Cannot read JSON file 'links_data.json': {e}")
        sys.exit(1)

    if not json_string:
        print("Error: JSON file 'links_data.json' is empty.")
        sys.exit(1)
    try:
        # Data from Supabase is an array: [{"primary_link": "...", "backup_link": "..."}, ...]
        api_data = json.loads(json_string)

        # Transform the array into the dictionary structure expected by the script: {"primary_link": "backup_link", ...}
        link_map = {
            item['primary_link']: item['backup_link'] 
            for item in api_data 
            if item.get('primary_link') and item.get('backup_link')
        }
        return link_map
    except (json.JSONDecodeError, TypeError, KeyError) as e:
        print(f"Error: Unable to process JSON data from the API. Error: {e}")
        print("Received data:", json_string)
        sys.exit(1)

def replace_links_in_file(file_path, link_map):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    replaced = 0
    for old, new in link_map.items():
        if old in content:
            content = content.replace(old, new)
            replaced += 1

    if replaced > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"{file_path}: {replaced} link(s) replaced")

def replace_links_in_repo(repo_path, link_map):
    print(f"Loaded {len(link_map)} link mappings")

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(('.md')):
                file_path = os.path.join(root, file)
                replace_links_in_file(file_path, link_map)

if __name__ == "__main__":
    repo_dir = os.getcwd()  # run from root repo
    target_dir = os.path.join(repo_dir, "docs")
    print(target_dir)
    link_map_from_api = get_link_map_from_api()
    replace_links_in_repo(target_dir, link_map_from_api)
    print("Completed replacing Drive links throughout the repo.")