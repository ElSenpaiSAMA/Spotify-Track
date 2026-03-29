import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from extract import get_top_tracks
from transform import transform
from load import load
from visualize import get_latest_top10, generate_chart


def run_pipeline(time_range="short_term"):
    print("=" * 50)
    print("SPOTIFY TOP TRACKS PIPELINE")
    print("=" * 50)

    print("\n[1/4] Extrayendo datos de Spotify...")
    get_top_tracks(time_range=time_range)

    print("\n[2/4] Transformando datos...")
    df = transform(time_range=time_range)

    print("\n[3/4] Cargando en base de datos...")
    load(df)

    print("\n[4/4] Generando gráfico...")
    top10 = get_latest_top10()
    generate_chart(top10)

    print("\n" + "=" * 50)
    print("Pipeline completado!")
    print("  Grafico PNG → charts/top10.png")
    print("  Grafico HTML → charts/top10.html")
    print("  Base de datos → data/spotify.db")
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()
