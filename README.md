# Online Retail Data Pipeline Project

โปรเจกต์นี้เป็นการสร้าง Data Pipeline ตั้งแต่โหลดข้อมูลจาก Kaggle → เก็บข้อมูลใน PostgreSQL ด้วย Docker → ทำความสะอาดข้อมูล → ส่งออกสู่ Google Sheets → นำไปสร้าง Dashboard บน Looker Studio

---

## วิธีรันโปรเจกต์ (How to Run the Project)

### 1. เริ่มรันฐานข้อมูล PostgreSQL ด้วย Docker
ใช้คำสั่ง:
docker compose up -d

### 2. เตรียมไฟล์ข้อมูล
นำไฟล์ data.csv จาก Kaggle วางที่:
projectx/data/data.csv

### 3. รัน Pipeline ทั้งหมด
คำสั่งนี้จะรัน ingest.py → transform.py → publish.py แบบต่อเนื่อง:
python run_pipeline.py

---

## Pipeline Components

### ingest.py
อ่านข้อมูลจาก CSV (100,000 แถวแรก) และบันทึกลงตาราง:
raw_data.online_retail_raw

### transform.py
ทำความสะอาดข้อมูล, ลบข้อมูลที่ไม่ถูกต้อง, เพิ่มคอลัมน์ Year / Month / TotalPrice แล้วบันทึกลงตาราง:
production.online_retail_clean

### publish.py
ดึงข้อมูลจาก production แล้วส่งขึ้น Google Sheets (ผ่าน Service Account)

### run_pipeline.py
สคริปต์รวมโปรเซสทั้งหมด รัน ingest → transform → publish ในคำสั่งเดียว

---

## Google API (Credentials)
ต้องมีไฟล์ credentials.json สำหรับเชื่อม Google Sheets  
ให้วางไฟล์นี้ไว้ในโฟลเดอร์โปรเจกต์ (ระดับเดียวกับ publish.py)

**ห้ามอัปไฟล์นี้ขึ้น GitHub**  
ต้องเพิ่มใน .gitignore ดังนี้:
credentials.json

---

## Dashboard (Looker Studio)
ข้อมูลที่ถูกส่งไป Google Sheets จะถูกใช้สร้าง Dashboard ที่ประกอบด้วย:
- ยอดขายตามประเทศ
- สินค้าขายดีที่สุด
- ลูกค้าซื้อเยอะที่สุด
- แนวโน้มยอดขายรายเดือน
- ตัวกรอง Country / Year

