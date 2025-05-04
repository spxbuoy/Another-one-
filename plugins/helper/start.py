from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

DB_PATH = "plugins/xcc_db/users.db"

def is_registered(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, username TEXT)")
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (str(user_id),))
        return cursor.fetchone() is not None

def register_user(user_id, username):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (str(user_id), username))
        conn.commit()

@Client.on_message(filters.command("start"))
async def start_ui(client, message: Message):
    user_id = message.from_user.id
    username = message.from_user.first_name or "User"

    registered = is_registered(user_id)
    if not registered:
        register_user(user_id, username)

    status = "✅ Registered" if registered else "⚠️ Not Registered"

    await message.reply_text(
        f"⌬ 𝑾𝑬𝑳𝑪𝑶𝑴𝑬 𝑻𝑶 𝑩𝑨𝑹𝑹𝒀 𝑩𝑶𝑻\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"• Hello, <b>{username}</b>!\n"
        f"• User ID: <code>{user_id}</code>\n"
        f"• Status: <b>{status}</b>\n"
        f"• Version: <b>1.1</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"Use the menu below to explore bot features.\n"
        f"For issues, contact @BarryxSupportBot.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⚡ Command Menu", callback_data="commands")],
            [InlineKeyboardButton("Register", callback_data="register")],
            [InlineKeyboardButton("Close", callback_data="close_ui")]
        ])
    )

@Client.on_callback_query(filters.regex("register"))
async def register_btn(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    username = callback_query.from_user.first_name or "User"

    if is_registered(user_id):
        await callback_query.message.edit_text(
            f"⚠️ Hey <b>{username}</b>, you're already registered.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="commands")]]),
            
        )
    else:
        register_user(user_id, username)
        await callback_query.message.edit_text(
            f"✅ Welcome <b>{username}</b>, you are now registered!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Go to Menu", callback_data="commands")]]),
            
        )

@Client.on_callback_query(filters.regex("close_ui"))
async def close_menu(client, callback_query):
    await callback_query.message.delete()
