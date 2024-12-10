# parser.py

import json
import os

def load_streaming_data(file_paths):
    """Load and parse the streaming data from multiple JSON files."""
    consolidated_data = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            consolidated_data.extend(data)
    return consolidated_data

def filter_out_episodes(data):
    """Filter out entries where 'episode_data' is not null."""
    
    return [entry for entry in data if entry.get('episode_name') is None]