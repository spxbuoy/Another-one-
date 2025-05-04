from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

@Client.on_callback_query(filters.regex("register"))
async def register_callback(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()

    if user:
        role, credits = user[3], user[2]
    else:
        role, credits = "Free", 100

    await callback_query.message.edit_text(
        f"[✅] Registration Complete!\n━━━━━━━━━━━━━━\n[🔹] Name: {first_name}\n[🔹] ID: {user_id}\n[🔹] Role: {role}\n[🔹] Credits: {credits}\n\nClick below to open commands!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Commands", callback_data="commands")]
        ])
    )