from collections import Counter
from typing import List, Dict, Tuple
from datetime import datetime

def calculate_time_span(data: List[Dict]) -> Tuple[datetime, datetime]:
    """Calculate the first and last timestamp in the dataset."""
    timestamps = [datetime.strptime(entry['ts'], "%Y-%m-%dT%H:%M:%SZ") for entry in data]
    return min(timestamps), max(timestamps)


def calculate_grand_total_minutes(data: List[Dict]) -> float:
    """Calculate the total minutes listened."""
    total_ms = sum(entry['ms_played'] for entry in data)
    return total_ms / 60000

def calculate_total_minutes(data: List[Dict]) -> float:
    """Calculate total minutes for 12 month period"""
    total = sum(entry['msPlayed'] for entry in data)
    return total / 60000

def calculate_top_artists(data: List[Dict], top_n: int = 5) -> List[Tuple[str, float]]:
    """Calculate the top N artists by total listening time in minutes."""
    artist_playtime = Counter()
    for entry in data:
        artist_playtime[entry['master_metadata_album_artist_name']] += entry['ms_played']
    return [(artist, ms_played / 60000) for artist, ms_played in artist_playtime.most_common(top_n)]

def calculate_top_artists_12m(data: List[Dict], top_n: int = 5) -> List[Tuple[str, float]]:
    """Calculate the top N artists by total listening time in minutes."""
    artist_playtime = Counter()
    for entry in data:
        artist_playtime[entry['artistName']] += entry['msPlayed']
    return [(artist, ms_played) for artist, ms_played in artist_playtime.most_common(top_n)]

def calculate_top_tracks(data: List[Dict], top_n: int = 5) -> List[Tuple[str, float]]:
    """Calculate the top N tracks by total listening time in minutes."""
    track_playtime = Counter()
    for entry in data:
        track_name = f"{entry['master_metadata_album_artist_name']} - {entry['master_metadata_track_name']}"
        track_playtime[track_name] += entry['ms_played']
    return [(track, ms_played / 60000) for track, ms_played in track_playtime.most_common(top_n)]

def calculate_top_tracks_12m(data: List[Dict], top_n: int = 5) -> List[Tuple[str, float]]:
    """Calculate the top N tracks by total listening time in minutes."""
    track_playtime = Counter()
    for entry in data:
        track_name = f"{entry['artistName']} - {entry['trackName']}"
        track_playtime[track_name] += entry['msPlayed']
    return [(track, ms_played) for track, ms_played in track_playtime.most_common(top_n)]

def filter_data_by_year(data: List[Dict], year: int) -> List[Dict]:
    """Filter the data for a specific year."""
    return [entry for entry in data if datetime.strptime(entry['ts'], "%Y-%m-%dT%H:%M:%SZ").year == year]

def calculate_annual_breakdown(data: List[Dict]) -> Dict[int, Dict]:
    """Generate an annual breakdown of listening data."""
    annual_data = {}

    for entry in data:
        # Get the year from the timestamp (assuming the format is consistent)
        timestamp = datetime.strptime(entry['ts'], "%Y-%m-%dT%H:%M:%SZ")
        year = timestamp.year

        if year not in annual_data:
            annual_data[year] = {
                'data': [],
                'total_minutes': 0,
                'top_artists': Counter(),
                'top_tracks': Counter()
            }

        # Append entry to year-specific data
        annual_data[year]['data'].append(entry)
        annual_data[year]['total_minutes'] += entry['ms_played'] / 60000  # Add minutes
        annual_data[year]['top_artists'][entry['master_metadata_album_artist_name']] += entry['ms_played']
        track_name = f"{entry['master_metadata_album_artist_name']} - {entry['master_metadata_track_name']}"
        annual_data[year]['top_tracks'][track_name] += entry['ms_played']

    # Process the results for each year
    for year, year_data in annual_data.items():
        year_data['top_artists'] = year_data['top_artists'].most_common(5)
        year_data['top_tracks'] = year_data['top_tracks'].most_common(5)

    return annual_data

def calculate_annual_breakdown(data: List[Dict], start_year: int, end_year: int) -> Dict[int, Dict]:
    """Generate an annual breakdown of listening data for a range of years."""
    annual_data = {}

    for year in range(start_year, end_year + 1):
        # Filter data for the specific year
        filtered_data = filter_data_by_year(data, year)

        if filtered_data:  # Only process if there is data for that year
            annual_data[year] = {
                'total_minutes': calculate_grand_total_minutes(filtered_data),
                'top_artists': calculate_top_artists(filtered_data),
                'top_tracks': calculate_top_tracks(filtered_data)
            }
    return annual_data

def display_annual_breakdown(annual_data: Dict[int, Dict]):
    """Display the annual breakdown."""
    for year, year_data in sorted(annual_data.items()):
        print(f"\n=== Year: {year} ===")
        print(f"Total Listening Time: {year_data['total_minutes']:.2f} minutes\n")

        # Print top artists
        print("Top 5 Artists:")
        for artist, minutes in year_data['top_artists']:
            print(f"{artist}: {minutes:.2f} minutes")

        # Print top tracks
        print("\nTop 5 Tracks:")
        for track, minutes in year_data['top_tracks']:
            print(f"{track}: {minutes:.2f} minutes")

    return annual_data
