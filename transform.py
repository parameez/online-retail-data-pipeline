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

# 1) อ่านข้อมูลจาก raw_data
query = "SELECT * FROM raw_data.online_retail_raw"
df = pd.read_sql(query, engine)

# 2) Cleaning เบื้องต้น
# ลบแถวที่ CustomerID ว่าง
df = df.dropna(subset=["CustomerID"])

# ลบแถวจำนวน <= 0 หรือราคาต่อหน่วย <= 0
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

# แปลงวันที่
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# สร้างคอลัมน์ TotalPrice = Quantity * UnitPrice
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

# สร้างคอลัมน์ Year, Month ไว้ใช้ทำ Dashboard
df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month

# 3) เขียนกลับไป schema production
table_name = "online_retail_clean"

df.to_sql(
    table_name,
    engine,
    schema="production",
    if_exists="replace",
    index=False
)

print("แปลงข้อมูลและบันทึกใน production เรียบร้อยแล้ว!")
