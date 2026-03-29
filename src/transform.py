import os
import json
import glob
import pandas as pd
from datetime import datetime


def load_latest_raw(time_range="short_term"):
    pattern = f"data/raw/top_tracks_{time_range}_*.json"
    files = sorted(glob.glob(pattern))

    if not files:
        raise FileNotFoundError(f"No se encontró ningún archivo raw para {time_range}")

    latest = files[-1]
    print(f"Cargando: {latest}")

    with open(latest, "r", encoding="utf-8") as f:
        return json.load(f)


def transform(time_range="short_term"):
    raw = load_latest_raw(time_range)

    rows = []
    for i, track in enumerate(raw["tracks"]):
        rows.append({
            "rank":         i + 1,
            "track":        track.get("name", "Unknown"),
            "artist":       track["artists"][0]["name"] if track.get("artists") else "Unknown",
            "album":        track["album"]["name"] if track.get("album") else "Unknown",
            "duration_sec": track.get("duration_ms", 0) // 1000,
            "explicit":     track.get("explicit", False),
            "spotify_url":  track.get("external_urls", {}).get("spotify", ""),
            "extracted_at": raw["extracted_at"],
            "time_range":   time_range,
        })

    df = pd.DataFrame(rows)

    df.loc[:, "track"]        = df["track"].str.strip()
    df.loc[:, "artist"]       = df["artist"].str.strip()
    df.loc[:, "extracted_at"] = pd.to_datetime(df["extracted_at"])
    df.loc[:, "duration_fmt"] = df["duration_sec"].apply(
        lambda s: f"{s // 60}:{s % 60:02d}"
    )

    os.makedirs("data/processed", exist_ok=True)
    filename = f"data/processed/top_tracks_{time_range}_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False, encoding="utf-8")

    print(f"Transformadas {len(df)} canciones → {filename}")
    print(df[["rank", "track", "artist", "duration_fmt"]].to_string(index=False))

    return df


if __name__ == "__main__":
    transform()