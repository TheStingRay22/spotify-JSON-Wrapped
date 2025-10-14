import json
from typing import List, Dict, Tuple
from datetime import datetime
import os

def load_streaming_data(file_paths):
    """Loads Streaming Data"""
    consolidated_data = []
    for file_path in file_paths:
        if not(os.path.exists(file_path)):
            print(f"File not found: {file_path}")
            continue
        if not file_path.lower().endswith('.json'):
            print(f"Skipping non-JSON file: {file_path}")
            continue
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if not isinstance(data, list):
                    print(f"Unexpected data format in file: {file_path}")
                    continue
                valid_entries = [
                    entry for entry in data
                    if isinstance(entry, dict) and 'ts' in entry and 'ms_played' in entry
                ]
                if not valid_entries:
                    print(f"No valid entries found in file: {file_path}")
                    continue
                consolidated_data.extend(valid_entries)
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {file_path}")
        except Exception as e:
            print(f"Unexpected error processing file {file_path}: {e}")
    if not consolidated_data:
        print("No valid data loaded from the provided files.")
    return consolidated_data

def filter_out_episodes(data):
    """Filter out entries where 'episode_data' is not null."""
    episode_free = [entry for entry in data if entry.get('episode_name') is None]
    broken_free = [entry for entry in episode_free if entry.get('master_metadata_track_name')is not None]
    return broken_free

def get_start_and_end_year(data: List[Dict]) -> Tuple[int, int]:
    """Get the starting and final years based on the data's timestamps."""
    years = [datetime.strptime(entry['ts'], "%Y-%m-%dT%H:%M:%SZ").year for entry in data]
    start_year = min(years)
    end_year = max(years)
    return start_year, end_year

def find_json_files(directory: str) -> list:
    """Recursively find all json files in a dir"""
    json_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files