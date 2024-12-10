from collections import Counter
from typing import List, Dict, Tuple
from datetime import datetime

def calculate_grand_total_minutes(data: List[Dict]) -> float:
    """Calculate the total minutes listened."""
    total_ms = sum(entry['ms_played'] for entry in data)
    return total_ms / 60000

def calculate_time_span(data: List[Dict]) -> Tuple[datetime, datetime]:
    """Calculate the first and last timestamp in the dataset."""
    timestamps = [datetime.strptime(entry['ts'], "%Y-%m-%dT%H:%M:%SZ") for entry in data]
    return min(timestamps), max(timestamps)

def calculate_listening_percentage(data: List[Dict], total_time_span: Tuple[datetime, datetime]) -> float:
    """Calculate the percentage of total time spent listening."""
    total_minutes = calculate_grand_total_minutes(data)
    time_span_minutes = (total_time_span[1] - total_time_span[0]).total_seconds() / 60
    return (total_minutes / time_span_minutes) * 100

def calculate_top_artists(data: List[Dict], top_n: int = 5) -> List[Tuple[str, float]]:
    """Calculate the top N artists by total listening time in minutes."""
    artist_playtime = Counter()
    for entry in data:
        artist_playtime[entry['master_metadata_album_artist_name']] += entry['ms_played']
    return [(artist, ms_played / 60000) for artist, ms_played in artist_playtime.most_common(top_n)]

def calculate_top_tracks(data: List[Dict], top_n: int = 5) -> List[Tuple[str, float]]:
    """Calculate the top N tracks by total listening time in minutes."""
    track_playtime = Counter()
    for entry in data:
        track_name = f"{entry['master_metadata_album_artist_name']} - {entry['master_metadata_track_name']}"
        track_playtime[track_name] += entry['ms_played']
    return [(track, ms_played / 60000) for track, ms_played in track_playtime.most_common(top_n)]