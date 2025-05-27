from pyrogram import Client, filters
from pyrogram.types import Message
import sqlite3
from datetime import datetime

DB_PATH = "plugins/xcc_db/users.db"

# Replace with your actual admin Telegram user IDs
ADMIN_IDS = [6440962840]

@Client.on_message(filters.command("reset", prefixes=["/", "."]) & filters.private)
async def reset_daily_command(client, message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.reply("❌ You are not authorized to run this command.")

    today = datetime.utcnow().strftime("%Y-%m-%d")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET daily_check_count = 0, last_check_date = ?
        """, (today,))
        conn.commit()

    await message.reply(f"✅ All users' daily check limits have been reset for {today}.")
