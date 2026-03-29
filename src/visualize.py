import os
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text


DB_PATH = "data/spotify.db"


def get_latest_top10():
    engine = create_engine(f"sqlite:///{DB_PATH}")

    with engine.connect() as conn:
        df = pd.read_sql(text("""
            SELECT rank, track, artist, duration_fmt
            FROM top_tracks
            WHERE extracted_at = (SELECT MAX(extracted_at) FROM top_tracks)
            ORDER BY rank ASC
            LIMIT 10
        """), conn)

    return df


def generate_chart(df: pd.DataFrame):
    df.loc[:, "label"] = df.apply(
        lambda r: f"#{r['rank']}  {r['track']} — {r['artist']}", axis=1
    )
    df.loc[:, "score"] = 51 - df["rank"]

    df = df.sort_values("rank", ascending=False)

    fig = px.bar(
        df,
        x="score",
        y="label",
        orientation="h",
        title="My Spotify Top 10 — Last 4 weeks",
        labels={"score": "Position", "label": ""},
        color="score",
        color_continuous_scale="Teal",
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=13),
        title_font_size=18,
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=60, b=40),
        height=450,
        width=800,
    )

    fig.update_xaxes(range=[0, 55], showgrid=True, gridcolor="#f0f0f0")
    fig.update_yaxes(tickfont=dict(size=12))

    os.makedirs("charts", exist_ok=True)
    fig.write_image("charts/top10.png")
    print("Gráfico guardado → charts/top10.png")
    fig.write_html("charts/top10.html")
    print("Gráfico interactivo → charts/top10.html")


if __name__ == "__main__":
    df = get_latest_top10()
    print(f"Top 10 cargado desde la base de datos ({len(df)} canciones)")
    generate_chart(df)