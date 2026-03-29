import pandas as pd
import pytest
from datetime import datetime


def make_sample_df():
    return pd.DataFrame([{
        "rank":         1,
        "track":        "Chichabeba",
        "artist":       "La Obsesion",
        "album":        "Chichabeba",
        "duration_sec": 195,
        "explicit":     False,
        "spotify_url":  "https://open.spotify.com/track/123",
        "extracted_at": datetime.now(),
        "time_range":   "short_term",
        "duration_fmt": "3:15",
    }])


def test_dataframe_has_required_columns():
    df = make_sample_df()
    required = ["rank", "track", "artist", "album", "duration_sec", "duration_fmt"]
    for col in required:
        assert col in df.columns


def test_rank_starts_at_one():
    df = make_sample_df()
    assert df["rank"].min() == 1


def test_duration_fmt_format():
    df = make_sample_df()
    assert ":" in df["duration_fmt"].iloc[0]


def test_no_empty_track_names():
    df = make_sample_df()
    assert df["track"].str.strip().ne("").all()


def test_no_empty_artist_names():
    df = make_sample_df()
    assert df["artist"].str.strip().ne("").all()