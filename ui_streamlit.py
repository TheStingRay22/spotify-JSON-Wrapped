import datetime
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
    # === Sidebar Filters & Controls === #    
    st.sidebar.header("Filters & Controls")
    
    # Extract available years
    years = sorted(set(
        pd.to_datetime([entry["ts"] for entry in music_data]).year
    ))
    min_year, max_year = min(years), max(years)
    
    # Year filter
    selected_years = st.sidebar.slider(
        "Select year range",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(int(min_year), int(max_year))
    )
    current_year = datetime.datetime.now().year
    
    st.sidebar.markdown("### Preset Filters")
    col_a, col_b, col_c = st.sidebar.columns(3)
    with col_a:
        if st.button("All Years"):
            selected_years = (int(min_year), int(max_year))
    with col_b:
        if st.button("Last Year"):
            selected_years = (current_year - 1, current_year - 1)
    with col_c:
        if st.button("This Year"):
            selected_years = (current_year, current_year)
    # Top - N Selector
    top_n = st.sidebar.selectbox(
        "Select Top Number for Artists and Tracks",
        options=[5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
        index=1
    )
    
    # Minimum listening Filter
    min_ms_played = st.sidebar.number_input(
        "Minimum Milliseconds Played to Include",
        min_value=0, max_value=60000, value=0, step=5000
    )
    # === Apply Filters ===
    filtered_data = [
    entry for entry in music_data
    if selected_years[0] <= pd.to_datetime(entry["ts"]).year <= selected_years[1]
    and entry["ms_played"] >= min_ms_played
    ]
    
    # Calculate and display stats
    start_year, end_year = get_start_and_end_year(filtered_data)
    total_minutes = calculate_grand_total_minutes(filtered_data)
    total_tracks = calculate_total_tracks(filtered_data)
    top_artists = calculate_top_artists(filtered_data, top_n=int(top_n))
    top_tracks = calculate_top_tracks(filtered_data, top_n=int(top_n))
    
    st.success(f"Analyzing {len(filtered_data)} plays from {start_year} to {end_year}")
    
    st.markdown(f"**Filters applied:** {selected_years[0]}–{selected_years[1]} | Top {top_n} | Min playtime: {min_ms_played} ms")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Tracks Played", total_tracks)
        st.metric("Total Minutes Listened", round(total_minutes))
    with col2:
        st.markdown("### Top Artists")
        
        artist_cols = st.columns(5) # gives us 5 artist per row
        for i, (artist_name, minutes_played) in enumerate(top_artists[:top_n]): # top N
            col = artist_cols[i % 5]
            with col:
                st.markdown(
                    f"""
                        <div style="
                                background-color:#f8f9fa;
                                border-radius:10px;
                                padding:10px;
                                display:flex;
                                flex-direction:column;
                                align-items:center;
                                justify-content:space-between;
                                text-align:center;
                                box-shadow:0 1px 3px rgba(0,0,0,0.1);
                                margin-bottom:10px;
                                height:300px;">
                            <img src="https://placehold.co/200x200?text=Art" 
                                alt="Artist image"
                                style="border-radius:50%; width:200px; height:200px; object-fit:cover;">
                            <h3 style="margin-top:10px; color:#111111;">{artist_name}</h3>
                            <p style="color:gray; font-size:20px;">{round(minutes_played, 1)} minutes</p>
                        </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("### Top Tracks")
        track_cols = st.columns(5)
        for i, (track_name, minutes_played) in enumerate(top_tracks[:10]):
            col = track_cols[i % 5]
            with col:
                st.markdown(
                    f"""
                        <div style="
                            background-color:#f8f9fa;
                            border-radius:10px;
                            padding:10px;
                            display:flex;
                            flex-direction:column;
                            align-items:center;
                            justify-content:space-between;
                            text-align:center;
                            box-shadow:0 1px 3px rgba(0,0,0,0.1);
                            margin-bottom:10px;
                            height:300px;">
                            <img src="https://placehold.co/200x200?text=Track" 
                                alt="Track image"
                                style="border-radius:10px; width:200px; height:200px; object-fit:cover;">
                            <h3 style="margin-top:10px; color:#111111;">{track_name}</h3>
                            <p style="color:gray; font-size:20px;">{round(minutes_played, 1)} minutes</p>
                        </div>
                    """,
                    unsafe_allow_html=True,
                )

else:
    st.info("Upload your Spotify JSON files to begin.")