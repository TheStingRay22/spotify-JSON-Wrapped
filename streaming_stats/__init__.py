# Package-level imports
from .parser import load_streaming_data
from .analytics import calculate_top_artists, calculate_top_tracks, calculate_total_minutes

# Package metadata
__version__ = "0.1.0"
__all__ = [
    "load_streaming_data",
    "calculate_top_artists",
    "calculate_top_tracks",
    "calculate_total_minutes",
]
