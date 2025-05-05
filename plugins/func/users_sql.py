import sqlite3
import random
import string
from datetime import date
from pyrogram import Client

# Create or recreate the table structure with all correct columns
def initialize_user_table():
    conn = sqlite3.connect('plugins/xcc_db/users.db')
    db = conn.cursor()
    db.execute("DROP TABLE IF EXISTS users")  # this clears old bad structure
    db.execute('''
        CREATE TABLE users (
            user_id TEXT PRIMARY KEY,
            username TEXT,
            status TEXT,
            plan TEXT,
            expiry TEXT,
            credits INTEGER,
            wait_time INTEGER,
            antispam_time TEXT,
            total_checks INTEGER,
            reg_date TEXT,
            totalkey TEXT DEFAULT '0'
        )
    ''')
    conn.commit()
    conn.close()

initialize_user_table()

# Generate random string
def randgen(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

# Register new user
def insert_reg_data(user_id, username, antispam_time, reg_at):
    conn = sqlite3.connect('plugins/xcc_db/users.db')
    db = conn.cursor()
    db.execute('''
        INSERT OR IGNORE INTO users (
            user_id, username, status, plan, expiry, credits, wait_time,
            antispam_time, total_checks, reg_date, totalkey
        ) VALUES (?, ?, 'FREE', 'N/A', 'N/A', 100, 30, ?, 0, ?, '0')
    ''', (str(user_id), username, antispam_time, reg_at))
    conn.commit()
    conn.close()

# Get full user data
def fetchinfo(user_id):
    conn = sqlite3.connect('plugins/xcc_db/users.db')
    db = conn.cursor()
    db.execute("SELECT * FROM users WHERE user_id = ?", (str(user_id),))
    info = db.fetchone()
    conn.close()
    return info

# Get all users
def getalldata(table_name):
    conn = sqlite3.connect('plugins/xcc_db/users.db')
    db = conn.cursor()
    db.execute(f"SELECT * FROM {table_name}")
    info = db.fetchall()
    conn.close()
    return info

# Rank based on user ID
def get_user_rank(user_id):
    if str(user_id) == "6440962840":
        return "Owner"
    return "Premium"

# Update specific column for user
def updatedata(user_id, column, value):
    conn = sqlite3.connect('plugins/xcc_db/users.db')
    db = conn.cursor()
    db.execute(f"UPDATE users SET {column} = ? WHERE user_id = ?", (value, str(user_id)))
    conn.commit()
    conn.close()

# Check expiry and downgrade if expired
async def plan_expirychk(user_id):
    try:
        today = str(date.today())
        plan_resp = fetchinfo(user_id)
        expiry = str(plan_resp[4])
        if expiry != 'N/A' and expiry < today:
            updatedata(user_id, "expiry", "N/A")
            updatedata(user_id, "plan", "N/A")
            await Client.send_message(user_id, "⛔ Your plan has expired. Use /buy to renew.")
    except Exception as e:
        print("Expiry check error:", e)
