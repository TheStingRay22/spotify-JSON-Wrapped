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

st.set_page_config(page_title="Spotify Super Wrapped", page_icon="🎧", layout="wide")

st.title("🎧 Spotify Super Wrapped")
st.markdown("Upload your Spotify streaming JSON files to see your listening stats!")

uploaded_files = st.file_uploader(
    "Upload one or more Spotify JSON files",
    type="json",
    accept_multiple_files=True
)

if uploaded_files:
    # Convert uploaded files to JSON objects
    json_data = []
    for uploaded_file in uploaded_files:
        try:
            data = json.load(uploaded_file)
            if isinstance(data, list):
                json_data.extend(data)
            else:
                st.warning(f"⚠️ {uploaded_file.name} did not contain a JSON list and was skipped.")
        except Exception as e:
            st.error(f"❌ Failed to parse {uploaded_file.name}: {e}")

    # Filter out episodes
    music_data = filter_out_episodes(json_data)
    if not music_data:
        st.error("No valid music data found in the uploaded files.")
        st.stop()

    start_year, end_year = get_start_and_end_year(music_data)
    total_minutes = calculate_grand_total_minutes(music_data)
    total_tracks = calculate_total_tracks(music_data)
    top_artists = calculate_top_artists(music_data, top_n=10)
    top_tracks = calculate_top_tracks(music_data, top_n=10)

    st.success(f"Analyzing {len(music_data)} plays from {start_year} to {end_year}")

    # Layout
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
    st.info("👆 Upload your Spotify JSON files to begin.")