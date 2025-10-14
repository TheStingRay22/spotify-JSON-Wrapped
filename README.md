# Spotify JSON Wrapped
## SPOTIFY HAS BEEN LYING TO US
![Doakes](https://i.tribune.com.pk/media/images/james-doakes1753344838-0/james-doakes1753344838-0-640x480.webp)


**Spotify JSON Wrapped** is a program for analyzing streaming history data from JSON files. It calculates and displays the top artists, top tracks, and total minutes played. This is directly from Spotify data, and if you compare it to your own 'Spotify Wrapped' it will not match.

## Current Release
[Release v1.0.0-Beta](https://github.com/TheStingRay22/spotify-JSON-Wrapped/releases/tag/v1.0.0-beta)

## New Features

### Core Functionality
- Parses one or more official Spotify streaming history JSON files.  
- Handles split exports and malformed data gracefully.  
- Filters out podcast and episode data automatically.  
- Outputs listening range, total minutes, total tracks, top artists, and top songs.

### Analytics Module
- Modular analytics pipeline designed for easy extension.  
- Calculates user-level statistics (listening totals, top rankings).  
- Provides annual breakdown support for future version upgrades.

### Streamlit Web Interface
- Lightweight, browser-based UI for uploading and viewing results.  
- Displays key metrics and sortable tables for artists and tracks.  
- Designed for quick local use or Streamlit Cloud deployment.

### Project Structure and Tooling
- Modular package under `streaming_stats/` for parser and analytics logic.  
- CLI version (`SpotifySuperWrapped.py`) preserved for command-line use.  
- Environment configuration via `.env` and `requirements.txt`.  
- Added full unit testing with `pytest` for parser and analytics functions.

---

## Installation

1. Collect your Data from Spotify [Link to Account data](https://www.spotify.com/us/account/privacy/)
3. Clone this repository or download the files.
```bash
  git clone https://github.com/<your_username>/spotify-JSON-Wrapped.git
  cd spotify-JSON-Wrapped
  pip install -r requirements.txt
  streamlit run ui_streamlit.py
```
4. Ensure you have Python 3.7+ installed on your system.
6. save all of your .json files to the same directory
7. delete any 'video'.json files
8. Upload to the streamlit web interface and prepare to be confused with spotify.

---

## Usage

**Web-Interface**
  ```bash
    streamlit run ui_streamlit.py
  ```
**CLI-Interface**
change the DEFAULTDIRECTORY variable at the top of `SpotifySuperWrapped.py` to your JSON data directory
  ```bash
  python SuperSpotifyWrapped.py
  ```

---

## Project Structure
```plaintext
spotify-JSON-Wrapped
├── streaming_stats
│   ├── __init__.py
│   ├── parser.py
│   ├── analytics.py
│   └── spotify_api.py
│
├── tests
│   ├── conftest.py
│   ├── test_parser.py
│   └── test_analytics.py
│
├── SpotifySuperWrapped.py
├── ui_streamlit.py
│
├── requirements.txt
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## License

This project is licensed under the MIT License. see LICENSE file for details.

---

## Credits
Created by TheStingRay22
[Github:TheStingRay22](https://github.com/TheStingRay22)

![me lmao](https://avatars.githubusercontent.com/u/122391911?v=4)

Please be nice I'm just a bored IT guy with free time and protien
