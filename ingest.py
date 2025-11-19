import pandas as pd
from sqlalchemy import create_engine

DB_USER = "kaggle_user"
DB_PASS = "kaggle_password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "kaggle_db"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

df = pd.read_csv("data/data.csv", nrows=100000, encoding="ISO-8859-1")

df.to_sql(
    "online_retail_raw",
    engine,
    schema="raw_data",
    if_exists="replace",
    index=False
)

print("Success: loaded to raw_data.online_retail_raw")
