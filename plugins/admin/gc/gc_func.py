import sqlite3
import random
import string

DB_PATH = "plugins/xcc_db/giftcard.db"

# Ensure gc table exists
def create_gc_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gc (
                id TEXT PRIMARY KEY,
                status TEXT,
                plan TEXT,
                credits INTEGER,
                days INTEGER
            )
        """)
        conn.commit()

create_gc_table()

# Generate code parts
def gcgenfunc(length=4):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

# INSERT with all fields
def insert_giftcode(gc: str, plan_type: str, credits: int, days: int):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO gc (id, status, plan, credits, days) VALUES (?, 'ACTIVE', ?, ?, ?)",
            (gc, plan_type, credits, days)
        )
        conn.commit()

# Helpers for other plans (if used elsewhere)
def insert_pm(gc): insert_giftcode(gc, "PREMIUM", 1000, 30)
def insert_plan1(gc): insert_giftcode(gc, "Starter", 1000, 7)
def insert_plan2(gc): insert_giftcode(gc, "Silver", 1500, 15)
def insert_plan3(gc): insert_giftcode(gc, "Gold", 3000, 30)

# Lookups
def getgc(gc: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gc WHERE id = ?", (gc,))
        return cursor.fetchone()

def getallgc():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gc")
        return cursor.fetchall()

def updategc(gc: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE gc SET status = 'USED' WHERE id = ?", (gc,))
        conn.commit()