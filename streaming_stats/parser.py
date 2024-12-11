""" 
Author: theStingray22

I wrote this module to convert the json data into a usable format and to strip the base data needed from this information to alleviate some of the analytics

Bad news for Spotify:
I woke up.
"""
import json
from typing import List, Dict, Tuple
from datetime import datetime
import os

def load_streaming_data(file_paths):
    """
    Loads in the data from the provided file

    Parameters
    ----------
    file_paths : file path
        A file path containing the .json files needed to extract the data from. 

    Returns
    -------
    list of dictionaries
        A list of dictionaries containing the extracted data.

    """
    consolidated_data = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            consolidated_data.extend(data)
    return [entry for entry in consolidated_data if entry.get('episode_name') is None]

def get_start_and_end_year(data: List[Dict]) -> Tuple[int, int]:
    """
    Calculates the start and end year from data

    Parameters
    ----------
    data : List of dict
        A list of dictionaries containing the entry "ts"

    Returns
    -------
    Tuple[int, int]
        A Tuple of two values (int) that represent the min and max years of data
    """
    years = [datetime.strptime(entry['ts'], "%Y-%m-%dT%H:%M:%SZ").year for entry in data]
    start_year = min(years)
    end_year = max(years)
    return start_year, end_year