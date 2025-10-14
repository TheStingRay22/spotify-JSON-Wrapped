# Spotify JSON Wrapped
## SPOTIFY HAS BEEN LYING TO US
![Pepe Silvia](https://i.kym-cdn.com/photos/images/newsfeed/002/546/187/fb1.jpg)


**Spotify JSON Wrapped** is a Python program for analyzing streaming history data from JSON files. It calculates and displays the top artists, top tracks, and total minutes played. This is directly from Spotify data, and if you compare it to your own 'Spotify Wrapped' it will not match.

***This is because Spotify is a***

![LIAR](https://media.tenor.com/oZrRoDQDXZ4AAAAe/anakin-liar.png)

## Features
- Analyze Spotify data and display it in the command line.
- Display the top artists and tracks based on playtime.
- Calculate total minutes played.
- calculate total *unique* songs played
- calculate total number of artists listened to
- Optional filtering by a start date. (12M only) *In-P for Super*
- Adjustable number of top artists and tracks to display (default: 5). (12M only) *IN-P for Super*

---

## Installation

1. Collect your Data from Spotify [Link to Account data](https://www.spotify.com/us/account/privacy/)
2. I reccomend selecting extended streaming history as it will work best. Alternatively [Spotify Wrapped 12M](SpotifyWrappedJSON12M.py) works very well for the basic account data.
3. Clone this repository or download the files.
4. Ensure you have Python 3.7+ installed on your system.
5. save all of your .json files to the same directory
6. delete any 'video'.json files
7. grab your spotify wrapped from years past and fume

---

## Usage

If you have just the small data the usage is very simple.
Enter your working directory and in the command line of your choice enter the following:

  ```bash
  python SpotifyWrappedJSON12M.py <files> [--start-date YYYY-MM-DD] [--top-n N]
  ```
Parameters are explained [below](#parameters)

If you opted (as you should) to get the extended data you will need to use [Super Spotify Wrapped](SuperSpotifyWrapped.py)
The first step is to change the [default directory Global Variable](https://github.com/TheStingRay22/spotify-JSON-Wrapped/blob/2836c8b8a64816594f77e8cc374f95704a2625c5/SpotifySuperWrapped.py#L15-L16) in the script
Then all you have to do is run the script in command line. you may have to work with your command line width to get it to display correctly.

  ```bash
  python SuperSpotifyWrapped.py
  ```



### Parameters: 
- `<files>`: Paths to one or more JSON files containing streaming history
- `--start-date` (optional): Start date for filtering records (format: YYYY-MM-DD).
- `--top-n` (optional): Numbner of top artists and tracks to display (default 5).

### Examples:
1. Analyze a single file with no filtering:
   ```bash
   python SpotifyWrappedJSON12M.py StreamingHistory_music_0.json
2. Analyze multiple files with a start date:
   ```bash
   python SpotifyWrappedJSON12M.py StreamingHistory_music_0.json StreamingHistory_music_1.json --start-date 2023-12-01
3. Display top 10 artists and tracks
   ```bash
   python SpotifyWrappedJSON12M.py StreamingHistory_music_0.json --top-n 10

---

## Project Structure
```plaintext
streaming_stats/
    __init__.py          # Package initialization
    parser.py            # Parses the JSON data and filers out the junk
    analytics.py         # Does the actual meat and potatoes of the package
SpotifyWrappedJSON12M.py # Use this is you dowwnloaded the small amount of data
SpotifySuperWrapped.py   # This right here is my BOY
README.md                # literally what you are in
```

---

## License

This project is licensed under the MIT License. see LICENSE file for details.

---

## Credits
Created by TheStingRay22
[Github:TheStingRay22](https://github.com/TheStingRay22)

![me lmao](https://avatars.githubusercontent.com/u/122391911?v=4)

Please be nice I'm just a bored IT guy with free time and whiskey
