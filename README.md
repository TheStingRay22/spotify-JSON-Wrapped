# Spotify JSON Wrapped
## SPOTIFY HAS BEEN LYING TO US
![Pepe Silvia](https://i.kym-cdn.com/photos/images/newsfeed/002/546/187/fb1.jpg)


**Spotify JSON Wrapped** is a Python tool for analyzing streaming history data from JSON files. It calculates and displays the top artists, top tracks, and total minutes played, with options for filtering by start date and customizing the number of results displayed.

## Features
- Analyze multiple JSON files of streaming history.
- Display the top artists and tracks based on playtime.
- Calculate total minutes played.
- Optional filtering by a start date.
- Adjustable number of top artists and tracks to display (default: 5).

---

## Installation

1. Clone this repository or download the files.
2. Ensure you have Python 3.7+ installed on your system.

---

## Usage

Run the script using the command line. Here is the syntax

  ```bash
  python cli.py <files> [--start-date YYYY-MM-DD] [--top-n N]
  ```

### Arguments: 
- `<files>`: Paths to one or more JSON files containing streaming history
- `--start-date` (optional): Start date for filtering records (format: YYYY-MM-DD).
- `--top-n` (optional): Numbner of top artists and tracks to display (default 5).

### Examples:
1. Analyze a single file with no filtering:
   ```bash
   python cli.py StreamingHistory_music_0.json
2. Analyze multiple files with a start date:
   ```bash
   python cli.py StreamingHistory_music_0.json StreamingHistory_music_1.json --start-date 2023-12-01
3. Display top 10 artists and tracks
   ```bash
   python cli.py StreamingHistory_music_0.json --top-n 10

---

## Project Structure
```plaintext
streaming_stats/
    __init__.py          # Package initialization
    parser.py            # JSON file parser
    analytics.py         # Data analysis functions
cli.py                   # Command Line Interface script
README.md                # Project documentation
requirements.txt         # Required Python packages (if any)
```

---

## License

This project is licensed under the MIT License. see LICENSE file for details.

---

## Credits
Created by TheStingRay22
[Github:TheStingRay22](https://github.com/TheStingRay22)
