import os
import pandas as pd
from sqlalchemy import create_engine, text


DB_PATH = "data/spotify.db"


def get_engine():
   
    os.makedirs("data", exist_ok=True)
    return create_engine(f"sqlite:///{DB_PATH}")


def load(df: pd.DataFrame):
    
    engine = get_engine()

    df.to_sql(
        name="top_tracks",
        con=engine,
        if_exists="append",   
        index=False
    )

    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM top_tracks")).scalar()
        last  = conn.execute(text("""
            SELECT track, artist, rank
            FROM top_tracks
            ORDER BY extracted_at DESC, rank ASC
            LIMIT 10
        """)).fetchall()

    print(f"Carga completada. Total de registros en la base de datos: {total}")
    print("\nTop 10 más reciente en la base de datos:")
    for row in last:
        print(f"  #{row[2]:>2}  {row[0]} — {row[1]}")


if __name__ == "__main__":
    from transform import transform
    df = transform()
    load(df)