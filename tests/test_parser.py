import os
import json
import tempfile
from streaming_stats.parser import load_streaming_data, filter_out_episodes, get_start_and_end_year

def test_load_valid_json():
    """Tests that valid JSON is loaded in properly"""
    Fake_Data = [
        {
    "ts": "2012-06-29T16:41:52Z",
    "ms_played": 5000,
    "master_metadata_track_name": "Track A"
  },
        {
    "ts": "2012-06-29T16:41:52Z",
    "ms_played": 5000,
    "master_metadata_track_name": "Track B"
  }
    ]
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
        json.dump(Fake_Data, tmp)
        tmp_path = tmp.name
    loaded = load_streaming_data([tmp_path])
    assert len(loaded) == len(Fake_Data)
    assert all('ts' in entry for entry in loaded)
    os.remove(tmp_path)
    
def test_load_invalid_json():
    """Tests that invalid JSON is handled gracefully"""
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
        tmp.write("{invalid_json: true}")
        tmp_path = tmp.name
    loaded = load_streaming_data([tmp_path])
    assert loaded == [] # should skip invalid
    os.remove(tmp_path)

def test_filter_out_episodes():
    """Ensure episodes and broken tracks are filtered out"""
    data = [
        {"ts": "2023-01-01T10:00:00Z", "ms_played": 1000, "episode_name": "Podcast 1"},
        {"ts": "2023-01-02T10:00:00Z", "ms_played": 1000, "master_metadata_track_name": "Track A", "episode_name": None}
    ]
    result = filter_out_episodes(data)
    assert len(result) == 1
    assert result[0]['master_metadata_track_name'] == "Track A"
    
def test_get_start_and_end_year():
    """Tests that start and end years are correctly identified"""
    data = [
        {'ts': '2020-01-01T00:00:00Z', 'ms_played': 1000},
        {'ts': '2021-06-15T12:30:00Z', 'ms_played': 2000},
        {'ts': '2019-12-31T23:59:59Z', 'ms_played': 1500}
    ]
    start_year, end_year = get_start_and_end_year(data)
    assert start_year == 2019
    assert end_year == 2021