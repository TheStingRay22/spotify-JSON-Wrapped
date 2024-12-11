import os
from turtle import clear
from streaming_stats.parser import load_streaming_data, get_start_and_end_year
from datetime import datetime
from typing import List, Tuple
from streaming_stats.analytics import (
    calculate_grand_total_minutes,
    calculate_time_span,
    calculate_top_artists,
    calculate_top_tracks,
    display_annual_breakdown,
    calculate_annual_breakdown,
    calculate_total_artist_SUPER
)
DEFAULT_DIRECTORY = "/Users/dgra228/Documents/Dev/Python_Files/Spotify Extended Streaming History"

def find_json_files(directory: str) -> list:
    """Find all JSON files in the given directory."""
    return [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.endswith(".json")
    ]

def main():
    art = [
    "   _____             _   _  __          _____                        __          __                             _ ",
    "  / ____|           | | (_)/ _|        / ____|                       \\ \\        / /                            | |",
    " | (___  _ __   ___ | |_ _| |_ _   _  | (___  _   _ _ __   ___ _ __   \\ \\  /\\  / / __ __ _ _ __  _ __   ___  __| |",
    "  \\___ \\| '_ \\ / _ \\| __| |  _| | | |  \\___ \\| | | | '_ \\ / _ \\ '__|   \\ \\/  \\/ / '__/ _` | '_ \\| '_ \\ / _ \\/ _` |",
    "  ____) | |_) | (_) | |_| | | | |_| |  ____) | |_| | |_) |  __/ |       \\  /\\  /| | | (_| | |_) | |_) |  __/ (_| |",
    " |_____/| .__/ \\___/ \\__|_|_|  \\__, | |_____/ \\__,_| .__/ \\___|_|        \\/  \\/ |_|  \\__,_| .__/| .__/ \\___|\\__,_|",
    "        | |                     __/ |              | |                                    | |   | |               ",
    "        |_|                    |___/               |_|                                    |_|   |_|               "

    ]
    for line in art:
        print(line)
    
    # Open file dialog to select files
    file_paths = find_json_files(DEFAULT_DIRECTORY)
    if not file_paths:
        print("No files selected. Exiting.")
        return

    data = load_streaming_data(file_paths)
    # print(f"Loaded {len(data)} records from {len(file_paths)} files.")
    start_year, end_year = get_start_and_end_year(data)
    total_minutes = calculate_grand_total_minutes(data)
    time_span = calculate_time_span(data)
    top_artists = calculate_top_artists(data)
    top_tracks = calculate_top_tracks(data)
    total_artist = calculate_total_artist_SUPER(data)

    print(f"Grand Total Minutes Listened: {total_minutes:>20,.2f}")
    print(f"Grand total artists listened to: {total_artist:>20,.0f}")
    print(f"Time Span: {time_span[0]} to {time_span[1]}")
    print("\nTop 5 Artists:")
    for artist, minutes in top_artists:
         print(f"{artist:<50}: {minutes:>20,.2f} minutes")
    print("\nTop 5 Tracks:")
    for track, minutes in top_tracks:
         print(f"{track:<50}: {minutes:>20,.2f} minutes")

    # Generate and display annual breakdown
    annual_data = calculate_annual_breakdown(data, start_year, end_year)
    display_annual_breakdown(annual_data)

if __name__ == "__main__":
    main()



   