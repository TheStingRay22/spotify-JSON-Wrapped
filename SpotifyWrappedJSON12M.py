import argparse
from pathlib import Path
from datetime import datetime
from streaming_stats.parser import load_streaming_data
from streaming_stats.analytics import calculate_top_artists_12m, calculate_top_tracks_12m, calculate_total_minutes, calculate_total_artists_12m

def main():
    parser = argparse.ArgumentParser(description="Analyze streaming history data.")
    parser.add_argument('files', nargs='+', type=Path, help="Paths to JSON streaming history files")
    parser.add_argument('--start-date', type=str, help="Start date for filtering data (format: YYYY-MM-DD)")
    parser.add_argument('--top-n', type=int, default=5, help="Number of top artists/tracks to display (default: 5)")
    args = parser.parse_args()

    # Load data
    data = load_streaming_data(args.files)

    # Filter data by start date if provided
    if args.start_date:
        try:
            start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
            data = [entry for entry in data if datetime.strptime(entry['endTime'], "%Y-%m-%d %H:%M") >= start_date]
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            return

    # Display results
    print("\n\n\n=== Top Artists ===")
    ArtistCounter = 1
    for artist, playtime in calculate_top_artists_12m(data, top_n=args.top_n):
        
        print(f"{ArtistCounter} {artist}: {playtime / 60000:.2f} minutes")
        ArtistCounter = ArtistCounter + 1

    print("\n=== Top Tracks ===")
    TrackCounter = 1
    for track, playtime in calculate_top_tracks_12m(data, top_n=args.top_n):

        print(f"{TrackCounter} {track}: {playtime / 60000:.2f} minutes")
        TrackCounter = TrackCounter + 1

    print(f"\n=== Total Minutes Played ===")
    print(f"You listened for {calculate_total_minutes(data):.2f} minutes")

    print(f"\n=== Total Artists ===")
    print(f"You listened to {calculate_total_artists_12m(data)} artists this year!\n\n")

if __name__ == "__main__":
    main()