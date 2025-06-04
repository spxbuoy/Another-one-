from plugins.func.users_sql import *
from datetime import datetime
import time

async def check_all_thing(Client, message):
    try:
        user_id = str(message.from_user.id)
        username = message.from_user.username or "None"

        regdata = fetchinfo(user_id)
        if not regdata:
            insert_reg_data(user_id, username, 0, str(datetime.today().date()))
            regdata = fetchinfo(user_id)

        role = regdata[2] or "FREE"
        wait_time = int(regdata[6] or (30 if role == "FREE" else 5))
        antispam_time = int(regdata[7] or 0)
        now = int(time.time())

        if now - antispam_time < wait_time:
            wait = wait_time - (now - antispam_time)
            await message.reply_text(f"⏳ AntiSpam: wait {wait}s", message.id)
            return [False, None]

        if regdata[1] == "BANNED":
            await message.reply_text("⛔ You are banned from using this bot.", message.id)
            return [False, None]

        return [True, role]

    except Exception as e:
        await message.reply_text("❌ Internal error occurred during check.")
        return [False, None]