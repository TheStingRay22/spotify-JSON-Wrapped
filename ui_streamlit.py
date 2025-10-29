import streamlit as st
import pandas as pd
import json
from streaming_stats.parser import load_streaming_data, filter_out_episodes, get_start_and_end_year
from streaming_stats.analytics import (
    calculate_top_artists,
    calculate_top_tracks,
    calculate_grand_total_minutes,
    calculate_total_tracks,
)
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = None
if "music_data" not in st.session_state:
    st.session_state.music_data = None

st.set_page_config(page_title="Spotify Super Wrapped", page_icon="🎧", layout="wide")

@st.cache_data(show_spinner=False)
def parse_uploaded_files(uploaded_files):
    """Parse uploaded files and return consolidated music data."""
    json_data = []
    for uploaded_file in uploaded_files:
        try:
            data = json.load(uploaded_file)
            if isinstance(data, list):
                json_data.extend(data)
        except Exception as e:
            st.error(f"Failed to parse {uploaded_file.name}: {e}")
    music_data = filter_out_episodes(json_data)
    return music_data

st.title("🎧 Spotify Super Wrapped")
st.markdown("Upload your Spotify streaming JSON files to see your listening stats!")

uploaded_files = st.file_uploader(
    "Upload your Spotify streaming history JSON files",
    type=["json"],
    accept_multiple_files=True,
)

#Reset button
if st.button("Reset Uploades"):
    st.session_state.clear()
    st.experimental_rerun()

if uploaded_files:
    st.session_state.uploaded_files = uploaded_files
    st.session_state.music_data = parse_uploaded_files(uploaded_files)
    
if st.session_state.music_data:
    music_data = st.session_state.music_data
    
    if not music_data:
        st.warning("No valid music data found in the uploaded files.")
        st.stop()

    # Calculate and display stats
    start_year, end_year = get_start_and_end_year(music_data)
    total_minutes = calculate_grand_total_minutes(music_data)
    total_tracks = calculate_total_tracks(music_data)
    top_artists = calculate_top_artists(music_data, top_n=10)
    top_tracks = calculate_top_tracks(music_data, top_n=10)
    
    st.success(f"Analyzing {len(music_data)} plays from {start_year} to {end_year}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Tracks Played", total_tracks)
        st.metric("Total Minutes Listened", round(total_minutes))
    with col2:
        st.markdown("### Top Artists")
        st.dataframe(pd.DataFrame(top_artists, columns=["Artist", "Minutes Played"]))

    st.markdown("### Top Tracks")
    st.dataframe(pd.DataFrame(top_tracks, columns=["Track", "Minutes Played"]))

else:
    st.info("Upload your Spotify JSON files to begin.")