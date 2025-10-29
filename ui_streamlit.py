import datetime
import streamlit as st
import pandas as pd
import json
import plotly.express as px
from streaming_stats.parser import load_streaming_data, filter_out_episodes, get_start_and_end_year
from streaming_stats.analytics import (
    calculate_top_artists,
    calculate_top_tracks,
    calculate_grand_total_minutes,
    calculate_total_tracks,
)

st.set_page_config(page_title="Spotify Super Wrapped", page_icon="🎧", layout="wide")

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = None
if "music_data" not in st.session_state:
    st.session_state.music_data = None
if "selected_years" not in st.session_state:
    st.session_state.selected_years = None
if "top_n" not in st.session_state:
    st.session_state.top_n = 10
if "min_ms_played" not in st.session_state:
    st.session_state.min_ms_played = 0

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
    key="file_uploader",
)

if st.button("Reset Uploads"):
    st.session_state.clear()
    st.experimental_rerun()

if uploaded_files:
    st.session_state.uploaded_files = uploaded_files
    st.session_state.music_data = parse_uploaded_files(uploaded_files)

music_data = st.session_state.music_data

if music_data:
    if not music_data:
        st.warning("No valid music data found in the uploaded files.")
        st.stop()

    # Extract available years
    years = sorted(set(pd.to_datetime([entry["ts"] for entry in music_data]).year))
    min_year, max_year = min(years), max(years)
    current_year = datetime.datetime.now().year

    # Sidebar Filters & Controls
    st.sidebar.header("Filters & Controls")

    # Year range slider with session state
    if st.session_state.selected_years is None:
        st.session_state.selected_years = (min_year, max_year)

    selected_years = st.sidebar.slider(
        "Select year range",
        min_value=int(min_year),
        max_value=int(max_year),
        value=st.session_state.selected_years,
        key="year_range_slider",
    )
    st.session_state.selected_years = selected_years

    # Preset filter buttons for years
    st.sidebar.markdown("### Preset Filters")
    col_a, col_b, col_c = st.sidebar.columns(3)
    with col_a:
        if st.button("All Years", key="preset_all_years"):
            st.session_state.selected_years = (min_year, max_year)
            st.experimental_rerun()
    with col_b:
        if st.button("Last Year", key="preset_last_year"):
            last_year = current_year - 1
            if last_year >= min_year:
                st.session_state.selected_years = (last_year, last_year)
                st.experimental_rerun()
    with col_c:
        if st.button("This Year", key="preset_this_year"):
            if current_year <= max_year:
                st.session_state.selected_years = (current_year, current_year)
                st.experimental_rerun()

    # Top-N selector with session state
    if st.session_state.top_n is None:
        st.session_state.top_n = 10
    top_n = st.sidebar.selectbox(
        "Select Top Number for Artists and Tracks",
        options=[5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
        index=[5,10,15,20,25,30,35,40,45,50].index(st.session_state.top_n) if st.session_state.top_n in [5,10,15,20,25,30,35,40,45,50] else 1,
        key="top_n_selector",
    )
    st.session_state.top_n = top_n

    # Minimum milliseconds played filter with session state
    if st.session_state.min_ms_played is None:
        st.session_state.min_ms_played = 0
    min_ms_played = st.sidebar.number_input(
        "Minimum Milliseconds Played to Include",
        min_value=0,
        max_value=60000,
        value=st.session_state.min_ms_played,
        step=5000,
        key="min_ms_input",
    )
    st.session_state.min_ms_played = min_ms_played

    # Filter data based on selections
    filtered_data = [
        entry for entry in music_data
        if st.session_state.selected_years[0] <= pd.to_datetime(entry["ts"]).year <= st.session_state.selected_years[1]
        and entry["ms_played"] >= st.session_state.min_ms_played
    ]

    if not filtered_data:
        st.warning("No data matches the selected filters.")
        st.stop()

    # Calculate statistics
    start_year, end_year = get_start_and_end_year(filtered_data)
    total_minutes = calculate_grand_total_minutes(filtered_data)
    total_tracks = calculate_total_tracks(filtered_data)
    top_artists = calculate_top_artists(filtered_data, top_n=top_n)
    top_tracks = calculate_top_tracks(filtered_data, top_n=top_n)

    st.success(f"Analyzing {len(filtered_data)} plays from {start_year} to {end_year}")

    st.markdown(f"**Filters applied:** {st.session_state.selected_years[0]}–{st.session_state.selected_years[1]} | Top {top_n} | Min playtime: {min_ms_played} ms")

    # Metrics row
    metrics_col1, metrics_col2, metrics_col3 = st.columns([1,1,3])
    with metrics_col1:
        st.metric("Total Tracks Played", total_tracks)
    with metrics_col2:
        st.metric("Total Minutes Listened", round(total_minutes))
    with metrics_col3:
        st.markdown("")

    # Layout for Top Artists and Top Tracks cards + charts
    top_section = st.container()
    with top_section:
        st.markdown("---")
        st.markdown("### Top Artists & Tracks Overview")

        # Cards for Top Artists
        st.markdown("#### Top Artists")
        artist_cols = st.columns(5)
        for i, (artist_name, minutes_played) in enumerate(top_artists[:top_n]):
            col = artist_cols[i % 5]
            with col:
                st.markdown(
                    f"""
                    <div style="
                        background-color:#f0f2f6;
                        border-radius:12px;
                        padding:15px;
                        text-align:center;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                        height:320px;
                        display:flex;
                        flex-direction:column;
                        justify-content:space-between;
                        ">
                        <img src="https://placehold.co/200x200?text=Art" 
                            alt="Artist image"
                            style="border-radius:50%; width:180px; height:180px; object-fit:cover; margin:auto;">
                        <h4 style="margin-top:15px; color:#111111; font-weight:600;">{artist_name}</h4>
                        <p style="color:#555555; font-size:18px; margin-bottom:0;">{round(minutes_played, 1)} minutes</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Cards for Top Tracks
        st.markdown("#### Top Tracks")
        track_cols = st.columns(5)
        for i, (track_name, minutes_played) in enumerate(top_tracks[:top_n]):
            col = track_cols[i % 5]
            with col:
                st.markdown(
                    f"""
                    <div style="
                        background-color:#f0f2f6;
                        border-radius:12px;
                        padding:15px;
                        text-align:center;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                        height:320px;
                        display:flex;
                        flex-direction:column;
                        justify-content:space-between;
                        ">
                        <img src="https://placehold.co/200x200?text=Track" 
                            alt="Track image"
                            style="border-radius:12px; width:180px; height:180px; object-fit:cover; margin:auto;">
                        <h4 style="margin-top:15px; color:#111111; font-weight:600;">{track_name}</h4>
                        <p style="color:#555555; font-size:18px; margin-bottom:0;">{round(minutes_played, 1)} minutes</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Prepare data for charts
    # Top Artists Bar Chart
    artists_df = pd.DataFrame(top_artists[:top_n], columns=["Artist", "Minutes Played"])
    fig_artists = px.bar(
        artists_df,
        x="Minutes Played",
        y="Artist",
        orientation="h",
        title="Top Artists by Minutes Played",
        labels={"Minutes Played": "Minutes Played", "Artist": "Artist"},
        text=artists_df["Minutes Played"].round(1),
        height=400,
    )
    fig_artists.update_layout(yaxis=dict(autorange="reversed"), margin=dict(l=100, r=20, t=40, b=40))
    fig_artists.update_traces(marker_color="#1DB954", textposition='outside')

    # Top Tracks Bar Chart
    tracks_df = pd.DataFrame(top_tracks[:top_n], columns=["Track", "Minutes Played"])
    fig_tracks = px.bar(
        tracks_df,
        x="Minutes Played",
        y="Track",
        orientation="h",
        title="Top Tracks by Minutes Played",
        labels={"Minutes Played": "Minutes Played", "Track": "Track"},
        text=tracks_df["Minutes Played"].round(1),
        height=400,
    )
    fig_tracks.update_layout(yaxis=dict(autorange="reversed"), margin=dict(l=100, r=20, t=40, b=40))
    fig_tracks.update_traces(marker_color="#1DB954", textposition='outside')

    # Listening Trends Line Chart
    # Aggregate total minutes per month
    df_dates = pd.DataFrame(filtered_data)
    df_dates["datetime"] = pd.to_datetime(df_dates["ts"])
    df_dates["year_month"] = df_dates["datetime"].dt.to_period("M").dt.to_timestamp()
    monthly_minutes = df_dates.groupby("year_month")["ms_played"].sum().reset_index()
    monthly_minutes["minutes"] = monthly_minutes["ms_played"] / 60000

    fig_trends = px.line(
        monthly_minutes,
        x="year_month",
        y="minutes",
        title="Listening Trends Over Time (Monthly)",
        labels={"year_month": "Month", "minutes": "Minutes Listened"},
        markers=True,
        height=400,
    )
    fig_trends.update_layout(margin=dict(l=40, r=40, t=40, b=40))
    fig_trends.update_traces(line_color="#1DB954")

    # Display charts in two columns
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.plotly_chart(fig_artists, use_container_width=True)
    with chart_col2:
        st.plotly_chart(fig_tracks, use_container_width=True)

    st.plotly_chart(fig_trends, use_container_width=True)

    # Custom CSS for overall styling
    st.markdown(
        """
        <style>
            /* Scrollbar for sidebar */
            ::-webkit-scrollbar {
                width: 8px;
            }
            ::-webkit-scrollbar-track {
                background: #f1f1f1; 
            }
            ::-webkit-scrollbar-thumb {
                background: #888; 
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #555; 
            }
            /* Hide Streamlit footer */
            footer {visibility: hidden;}
            /* Title styling */
            .css-1v3fvcr h1 {
                font-weight: 700;
                color: #1DB954;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

else:
    st.info("Upload your Spotify JSON files to begin.")