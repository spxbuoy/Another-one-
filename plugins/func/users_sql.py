import sqlite3
import random
import string
from datetime import date
from pyrogram import Client

def randgen(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

def insert_reg_data(user_id, username, antispam_time, reg_at):
    conn = sqlite3.connect('plugins/xcc_db/users.db')
    db = conn.cursor()
    db.execute("INSERT INTO users VALUES (?, ?, 'FREE', 'N/A', 'N/A', '100', '30', ?, '0', ?)", 
               (str(user_id), username, antispam_time, reg_at))
    conn.commit()
    conn.close()

def fetchinfo(user_id):
    conn = sqlite3.connect('plugins/xcc_db/users.db')
    db = conn.cursor()
    db.execute("SELECT * FROM users WHERE user_id = ?", (str(user_id),))
    info = db.fetchone()
    conn.close()
    return info

def getalldata(table_name):
    conn = sqlite3.connect('plugins/xcc_db/users.db')
    db = conn.cursor()
    db.execute(f"SELECT * FROM {table_name}")
    info = db.fetchall()
    conn.close()
    return info

def get_user_rank(user_id):
    if str(user_id) == "6440962840":
        return "Owner"
    return "Premium"

def updatedata(user_id, column, value):
    conn = sqlite3.connect('plugins/xcc_db/users.db')
    db = conn.cursor()
    db.execute(f"UPDATE users SET {column} = ? WHERE user_id = ?", (value, str(user_id)))
    conn.commit()
    conn.close()

async def plan_expirychk(user_id):
    try:
        today = str(date.today())
        plan_resp = fetchinfo(user_id)
        expiry = str(plan_resp[4])
        if expiry != 'N/A' and expiry < today:
            updatedata(user_id, "expiry", "N/A")
            updatedata(user_id, "plan", "N/A")
            resp = """
𝗛𝗲𝘆 𝗗𝘂𝗱𝗲
𝗬𝗼𝘂𝗿 𝗣𝗹𝗮𝗻 𝗛𝗮𝘀 𝗘𝘅𝗽𝗶𝗿𝗲𝗱. 𝗣𝗹𝗲𝗮𝘀𝗲 𝗣𝘂𝗿𝗰𝗵𝗮𝘀𝗲 𝗔𝗴𝗮𝗶𝗻 𝘂𝘀𝗶𝗻𝗴 /buy
            """
            await Client.send_message(user_id, resp)
    except Exception as e:
        print(e)
