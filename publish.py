import pandas as pd
from sqlalchemy import create_engine

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe


DB_USER = "kaggle_user"
DB_PASS = "kaggle_password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "kaggle_db"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

query = "SELECT * FROM production.online_retail_clean"
df = pd.read_sql(query, engine)

print(f"โหลดข้อมูลจาก Postgres มาได้ {len(df)} แถว")

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)


SPREADSHEET_NAME = "Online_Retail_Dashboard"
WORKSHEET_NAME = "data"

sh = client.open(SPREADSHEET_NAME)

try:
    worksheet = sh.worksheet(WORKSHEET_NAME)
except gspread.exceptions.WorksheetNotFound:
    worksheet = sh.add_worksheet(title=WORKSHEET_NAME, rows="1000", cols="20")


worksheet.clear()

set_with_dataframe(worksheet, df)

print("อัปโหลดข้อมูลไปยัง Google Sheets เรียบร้อยแล้ว ✅")
