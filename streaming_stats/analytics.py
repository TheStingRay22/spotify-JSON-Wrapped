from collections import Counter
from typing import List, Dict, Tuple

def calculate_top_artists(data: List[Dict], top_n: int = 5) -> List[Tuple[str, int]]:
    """Returns the top N artists by playtime."""
    artist_playtime = Counter()
    for entry in data:
        artist_playtime[entry['artistName']] += entry['msPlayed']
    return artist_playtime.most_common(top_n)

def calculate_top_tracks(data: List[Dict], top_n: int = 5) -> List[Tuple[str, int]]:
    """Returns the top N tracks by playtime."""
    track_playtime = Counter()
    for entry in data:
        track_name = f"{entry['trackName']} - {entry['artistName']}"
        track_playtime[track_name] += entry['msPlayed']
    return track_playtime.most_common(top_n)

def calculate_total_minutes(data: List[Dict]) -> float:
    """Calculates total minutes played."""
    total_ms = sum(entry['msPlayed'] for entry in data)
    return total_ms / 60000