"""
spotify_api.py
Handles Spotify OAuth and data retrieval for artist and track metadata.
"""
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheFileHandler
import streamlit as st
from spotipy.cache_handler import CacheFileHandler

CACHE_DIR = os.path.join(os.getcwd(), ".cache_spotify")
os.makedirs(CACHE_DIR, exist_ok=True)

# Load environment variables
load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

SCOPE = "user-read-private user-top-read playlist-modify-public playlist-modify-private"

# Cache tokens in .cache_spotify/ directory (per user)
CACHE_DIR = os.path.join(os.getcwd(), ".cache_spotify")
os.makedirs(CACHE_DIR, exist_ok=True)

# --- Spotify Auth Setup ---
def get_spotify_auth():
    cache_handler = CacheFileHandler(cache_path=os.path.join(CACHE_DIR, "spotify_token.json"))
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        cache_handler=cache_handler,
        show_dialog=False,
    )


def get_spotify_client():
    """Authenticate automatically and return a Spotify client."""
    auth_manager = get_spotify_auth()
    token_info = auth_manager.get_cached_token()

    # If token already cached
    if token_info:
        return spotipy.Spotify(auth_manager=auth_manager)

    # No token yet — begin authorization
    auth_url = auth_manager.get_authorize_url()
    st.markdown("### 🔑 Connect to Spotify")
    st.markdown(f"[Authorize Spotify Account]({auth_url})")

    # Wait for Spotify redirect with ?code=... in URL
    params = st.query_params  # New API replaces experimental_get_query_params
    if "code" in params:
        code = params["code"]
        token_info = auth_manager.get_access_token(code)
        st.query_params.clear()  # Clears the URL query string
        st.success("Spotify authorization complete! Reloading...")
        st.rerun()

    return None

    # Return authenticated Spotify client
    return spotipy.Spotify(auth_manager=auth_manager)


# --- Spotify API Wrappers ---
def get_artist_image_and_genres(sp, artist_name):
    """Fetch an artist’s image URL and genres."""
    try:
        results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
        if results["artists"]["items"]:
            artist = results["artists"]["items"][0]
            image_url = artist["images"][0]["url"] if artist["images"] else None
            genres = artist["genres"]
            return image_url, genres
    except Exception as e:
        st.error(f"Error fetching artist {artist_name}: {e}")
    return None, []


def get_track_image(sp, track_name, artist_name=None):
    """Fetch a track’s album cover image."""
    query = f"track:{track_name}"
    if artist_name:
        query += f" artist:{artist_name}"
    try:
        results = sp.search(q=query, type="track", limit=1)
        if results["tracks"]["items"]:
            track = results["tracks"]["items"][0]
            image_url = track["album"]["images"][0]["url"] if track["album"]["images"] else None
            return image_url
    except Exception as e:
        st.error(f"Error fetching track {track_name}: {e}")
    return None