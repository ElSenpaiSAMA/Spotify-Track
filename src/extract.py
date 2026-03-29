import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_top_tracks(limit=50, time_range="short_term"):

    cache_data = os.getenv("SPOTIPY_CACHE")
    if cache_data:
        with open(".cache", "w") as f:
            f.write(cache_data)

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-top-read",
        cache_path=".cache"
    ))

    results = sp.current_user_top_tracks(limit=limit, time_range=time_range)

    raw_data = {
        "extracted_at": datetime.now().isoformat(),
        "time_range": time_range,
        "tracks": results["items"]
    }

    os.makedirs("data/raw", exist_ok=True)
    filename = f"data/raw/top_tracks_{time_range}_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)

    print(f"Extraídas {len(results['items'])} canciones → {filename}")
    return filename


if __name__ == "__main__":
    get_top_tracks()