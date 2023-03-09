from fastapi import FastAPI
import pandas as pd
from sqlalchemy import create_engine, text


DATABASE_URL = "postgresql://znckjdyz:1Z1UVKsGHICvNknjnOSrzw3mlNjnN1jn@trumpet.db.elephantsql.com/znckjdyz"
engine = create_engine(DATABASE_URL)

app = FastAPI()


@app.get("/poi/{latitude}/{longitude}/{days}")
def poi(latitude: float, longitude: float, days: int):
    sql = (
        "WITH n AS (SELECT id FROM clusters "
        f"ORDER BY earth_distance(ll_to_earth(latitude, longitude), ll_to_earth({latitude}, {longitude})) "
        f"LIMIT {days}) "
        "SELECT p.* FROM n JOIN poi p ON p.cluster_id = n.id"
    )
    with engine.begin() as connection:
        return pd.read_sql(text(sql), connection).to_json(orient="records")


@app.get("/communes")
def communes():
    sql = "SELECT * FROM communes"
    with engine.begin() as connection:
        return pd.read_sql(text(sql), connection).to_json(orient="records")
