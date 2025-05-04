import sqlite3
import random
import string

DB_PATH = "plugins/xcc_db/giftcard.db"

# RANDOM GEN FUNCTION
def gcgenfunc(length=4):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


# Insert Gift Code into DB with specific plan type
def insert_giftcode(gc: str, plan_type: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO gc (id, status, plan) VALUES (?, 'ACTIVE', ?)", (gc, plan_type))
        conn.commit()

def insert_pm(gc): insert_giftcode(gc, "PREMIUM")
def insert_plan1(gc): insert_giftcode(gc, "PLAN1")
def insert_plan2(gc): insert_giftcode(gc, "PLAN2")
def insert_plan3(gc): insert_giftcode(gc, "PLAN3")


# Get single gift card by code
def getgc(gc: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gc WHERE id = ?", (gc,))
        return cursor.fetchone()


# Get all gift cards
def getallgc():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gc")
        return cursor.fetchall()


# Mark a gift card as used
def updategc(gc: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE gc SET status = 'USED' WHERE id = ?", (gc,))
        conn.commit()