"""
spotify_api.py
Future home of API logic
"""
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")


def placeholder():
    return "Spotify API Integration is on its way!"