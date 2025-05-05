from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import date
from plugins.func.users_sql import fetchinfo, insert_reg_data

@Client.on_message(filters.command("register"))
async def register_user(client: Client, message: Message):
    user_id = str(message.from_user.id)
    username = message.from_user.first_name or "User"
    reg_date = str(date.today())  # Correctly format registration date

    # Check if user is already registered
    existing = fetchinfo(user_id)
    if existing:
        return await message.reply_text(
            f"⚠️ Hey <b>{username}</b>, you're already registered in our system!",
            quote=True
        )

    # Register new user with 200 credits and current date
    insert_reg_data(user_id, username, credits=200, reg_date=reg_date)

    await message.reply_text(
        f"✅ <b>Registration Successful!</b>\n\n"
        f"• Name: <code>{username}</code>\n"
        f"• User ID: <code>{user_id}</code>\n"
        f"• Plan: FREE\n"
        f"• Credits: 200\n"
        f"• Registered At: <code>{reg_date}</code>",
        quote=True
    )