from streaming_stats.analytics import (
    calculate_grand_total_minutes,
    calculate_top_artists,
    calculate_top_tracks,
    calculate_total_artist_SUPER,
    calculate_total_tracks
)

def mock_data():
    return [
        {"ts": "2023-01-01T00:00:00Z", "ms_played": 120000, "master_metadata_album_artist_name": "Artist A", "master_metadata_track_name": "Track A"},
        {"ts": "2023-01-02T00:00:00Z", "ms_played": 60000, "master_metadata_album_artist_name": "Artist B", "master_metadata_track_name": "Track B"},
        {"ts": "2023-01-03T00:00:00Z", "ms_played": 180000, "master_metadata_album_artist_name": "Artist A", "master_metadata_track_name": "Track C"},
    ]

def test_total_minutes():
    total = calculate_grand_total_minutes(mock_data())
    assert round(total, 2) == 6.0  # 360000 ms / 60000

def test_top_artists():
    top = calculate_top_artists(mock_data(), top_n=1)
    assert top[0][0] == "Artist A"

def test_top_tracks():
    top = calculate_top_tracks(mock_data(), top_n=1)
    assert isinstance(top[0][0], str)

def test_total_artist_super():
    total = calculate_total_artist_SUPER(mock_data())
    assert total == 2

def test_total_tracks():
    total = calculate_total_tracks(mock_data())
    assert total == 3