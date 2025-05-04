import sqlite3

# Connect to your actual DB file
conn = sqlite3.connect("users.db")  # file is in same folder as shown
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE users ADD COLUMN antispam_time INTEGER DEFAULT 0;")
    print("✅ Column 'antispam_time' added.")
except Exception as e:
    print("⚠️ Maybe already added or failed:", e)

conn.commit()
conn.close()