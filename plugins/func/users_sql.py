import sqlite3
import random
import string
from datetime import date
from pyrogram import Client

DB_PATH = 'plugins/xcc_db/users.db'

# Auto-create users table if it doesn't exist
def initialize_user_table():
    conn = sqlite3.connect(DB_PATH)
    db = conn.cursor()
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
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

# Random generator
def randgen(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

# Register new user
def insert_reg_data(user_id, username, antispam_time, reg_at):
    conn = sqlite3.connect(DB_PATH)
    db = conn.cursor()
    db.execute("INSERT OR IGNORE INTO users VALUES (?, ?, 'FREE', 'N/A', 'N/A', 100, 30, ?, 0, ?, '0')",
               (str(user_id), username, antispam_time, reg_at))
    conn.commit()
    conn.close()

# Fetch user info
def fetchinfo(user_id):
    conn = sqlite3.connect(DB_PATH)
    db = conn.cursor()
    db.execute("SELECT * FROM users WHERE user_id = ?", (str(user_id),))
    info = db.fetchone()
    conn.close()
    return info

# Get all users from a table
def getalldata(table_name):
    conn = sqlite3.connect(DB_PATH)
    db = conn.cursor()
    db.execute(f"SELECT * FROM {table_name}")
    info = db.fetchall()
    conn.close()
    return info

# Update single column for user
def updatedata(user_id, column, value):
    conn = sqlite3.connect(DB_PATH)
    db = conn.cursor()
    db.execute(f"UPDATE users SET {column} = ? WHERE user_id = ?", (value, str(user_id)))
    conn.commit()
    conn.close()

# Get user rank
def get_user_rank(user_id):
    return "Owner" if str(user_id) == "6440962840" else "Premium"

# Check if plan expired
async def plan_expirychk(user_id):
    try:
        today = str(date.today())
        plan_resp = fetchinfo(user_id)
        if not plan_resp:
            return
        expiry = str(plan_resp[4])
        if expiry != 'N/A' and expiry < today:
            updatedata(user_id, "expiry", "N/A")
            updatedata(user_id, "plan", "N/A")
            await Client.send_message(user_id,
                "𝗛𝗲𝘆 𝗗𝘂𝗱𝗲\n𝗬𝗼𝘂𝗿 𝗣𝗹𝗮𝗻 𝗛𝗮𝘀 𝗘𝘅𝗽𝗶𝗿𝗲𝗱.\n𝗣𝗹𝗲𝗮𝘀𝗲 𝗣𝘂𝗿𝗰𝗵𝗮𝘀𝗲 𝗔𝗴𝗮𝗶𝗻 𝘂𝘀𝗶𝗻𝗴 /buy"
            )
    except Exception as e:
        print(f"Plan check error: {e}")
