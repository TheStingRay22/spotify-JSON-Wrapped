import json
from typing import List, Dict, Tuple
from datetime import datetime
import os

def load_streaming_data(file_paths):
    consolidated_data = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            consolidated_data.extend(data)
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