import json
from pathlib import Path
from typing import List, Dict

def load_streaming_data(file_paths: List[Path]) -> List[Dict]:
    """Loads and consolidates streaming data from multiple JSON files."""
    consolidated_data = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            consolidated_data.extend(data)
    return consolidated_data
