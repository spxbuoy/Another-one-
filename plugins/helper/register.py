from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
import time
from plugins.func.users_sql import fetchinfo, insert_reg_data

@Client.on_message(filters.command("register"))
async def register_user(client, message: Message):
    user_id = str(message.from_user.id)
    username = message.from_user.first_name or "User"
    reg_time = str(datetime.now().date())
    antispam_time = int(time.time())

    # Check if user already exists
    existing = fetchinfo(user_id)
    if existing:
        return await message.reply_text(
    f"⚠️ Hey <b>{username}</b>, you're already registered in our database!",
    
)

    # Register the user
    insert_reg_data(user_id, username, antispam_time, reg_time)
    await message.reply_text(
        f"✅ <b>Registration successful!</b>\n\n"
        f"• Name: <code>{username}</code>\n"
        f"• User ID: <code>{user_id}</code>\n"
        f"• Plan: FREE\n"
        f"• Credits: 100",
        
    )
