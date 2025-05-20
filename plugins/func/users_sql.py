import sqlite3
import os
from datetime import date

# === Paths ===
DB_FOLDER = "plugins/xcc_db"
DB_PATH = os.path.join(DB_FOLDER, "users.db")
CUSTOMER_DB = os.path.join(DB_FOLDER, "customer.db")

# === Ensure folder exists ===
os.makedirs(DB_FOLDER, exist_ok=True)

# === Init DBs ===
def init_databases():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT,
                status TEXT,
                plan TEXT,
                expiry TEXT,
                credits INTEGER,
                wait_time INTEGER,
                antispam_time INTEGER,
                total_checks INTEGER,
                reg_date TEXT,
                totalkey INTEGER
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_gates (
                user_id TEXT PRIMARY KEY,
                site_url TEXT,
                proxy TEXT
            )
        """)
        conn.commit()

    with sqlite3.connect(CUSTOMER_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS premium_users (
                user_id TEXT PRIMARY KEY,
                username TEXT,
                plan TEXT,
                credits INTEGER,
                expiry TEXT
            )
        """)
        conn.commit()

# === Register a new user ===
def insert_reg_data(user_id, username, credits=200, reg_date=str(date.today())):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO users (
                user_id, username, status, plan, expiry, credits,
                wait_time, antispam_time, total_checks, reg_date, totalkey
            ) VALUES (?, ?, 'FREE', 'None', 'None', ?, 15, 0, 0, ?, 0)
        """, (user_id, username, credits, reg_date))
        conn.commit()

# === Fetch user info ===
def fetchinfo(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()

# === Update any user field ===
def updatedata(user_id, field, value):
    allowed = {
        "username", "status", "plan", "expiry", "credits", "wait_time",
        "antispam_time", "total_checks", "reg_date", "totalkey"
    }
    if field not in allowed:
        raise ValueError("Invalid field name")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET {field} = ? WHERE user_id = ?", (value, user_id))
        conn.commit()

# === Check plan expiry and sync with customer DB ===
def plan_expirychk(user_id=None):
    with sqlite3.connect(DB_PATH) as user_conn, sqlite3.connect(CUSTOMER_DB) as cust_conn:
        u_cursor = user_conn.cursor()
        c_cursor = cust_conn.cursor()

        if user_id:
            u_cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        else:
            u_cursor.execute("SELECT * FROM users")

        for row in u_cursor.fetchall():
            uid, uname, status, plan, expiry, credits, *_ = row
            if expiry != "None":
                try:
                    exp_date = date.fromisoformat(expiry)
                    if date.today() > exp_date:
                        u_cursor.execute("UPDATE users SET status='FREE', plan='None', expiry='None' WHERE user_id = ?", (uid,))
                        c_cursor.execute("DELETE FROM premium_users WHERE user_id = ?", (uid,))
                    else:
                        c_cursor.execute("""
                            INSERT OR REPLACE INTO premium_users (user_id, username, plan, credits, expiry)
                            VALUES (?, ?, ?, ?, ?)
                        """, (uid, uname, plan, credits, expiry))
                except:
                    continue
        user_conn.commit()
        cust_conn.commit()

# === Gate Functions ===
def set_user_gate(user_id, site_url, proxy):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            REPLACE INTO user_gates (user_id, site_url, proxy) VALUES (?, ?, ?)
        """, (user_id, site_url, proxy))
        conn.commit()

def get_user_gate(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT site_url, proxy FROM user_gates WHERE user_id = ?", (user_id,))
        return cursor.fetchone()

def remove_user_gate(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_gates WHERE user_id = ?", (user_id,))
        conn.commit()

# === Get all user data ===
def getalldata():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

# === Get stats: total users & premium ===
def get_user_stats():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

    with sqlite3.connect(CUSTOMER_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM premium_users")
        premium_users = cursor.fetchone()[0]

    return total_users, premium_users

# === Set anti-spam time ===
def setantispamtime(user_id):
    import time
    now = int(time.time())
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET antispam_time = ? WHERE user_id = ?", (now, user_id))
        conn.commit()

# === Deduct credits ===
def massdeductcredit(user_id, amount):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET credits = credits - ? WHERE user_id = ?", (amount, user_id))
        conn.commit()

def delete_user(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()

# === Init on import ===
init_databases()
