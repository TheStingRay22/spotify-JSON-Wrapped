import os
from tkinter import filedialog, Tk
from streaming_stats.parser import load_streaming_data
from streaming_stats.analytics import (
    calculate_grand_total_minutes,
    calculate_time_span,
    calculate_listening_percentage,
    calculate_top_artists,
    calculate_top_tracks
)

def open_files():
    """Open a file dialog to select multiple JSON files."""
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    file_paths = filedialog.askopenfilenames(
        title="Select Your Spotify Streaming History Files",
        filetypes=[("JSON files", "*.json")]
    )
    return list(file_paths)

def main():
    print("Welcome to Spotify Super Wrapped!")
    
    # Open file dialog to select files
    file_paths = open_files()
    if not file_paths:
        print("No files selected. Exiting.")
        return

    # Load and parse data
    data = load_streaming_data(file_paths)
    print(f"Loaded {len(data)} records from {len(file_paths)} files.")

    # Calculate analytics
    total_minutes = calculate_grand_total_minutes(data)
    time_span = calculate_time_span(data)
    listening_percentage = calculate_listening_percentage(data, time_span)
    top_artists = calculate_top_artists(data)
    top_tracks = calculate_top_tracks(data)

    # Display results
    print("\n=== Spotify Super Wrapped ===")
    print(f"Grand Total Minutes Listened: {total_minutes:.2f}")
    print(f"Time Span: {time_span[0]} to {time_span[1]}")
    print(f"Percentage of Time Spent Listening: {listening_percentage:.2f}%")
    print("\nTop 5 Artists:")
    for artist, minutes in top_artists:
        print(f"{artist}: {minutes:.2f} minutes")
    print("\nTop 5 Tracks:")
    for track, minutes in top_tracks:
        print(f"{track}: {minutes:.2f} minutes")

if __name__ == "__main__":
    main()