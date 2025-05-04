import os
import sqlite3

# Make sure directory exists
os.makedirs("plugins/xcc_db", exist_ok=True)

# Now connect to DB
conn = sqlite3.connect("plugins/xcc_db/users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    username TEXT,
    plan TEXT,
    expiry TEXT,
    role TEXT,
    credit TEXT,
    "limit" TEXT,
    antispam_time TEXT,
    total_hits TEXT,
    reg_at TEXT
)
""")

conn.commit()
conn.close()
print("✅ Fixed: users table created.")