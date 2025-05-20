from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from plugins.func.users_sql import insert_reg_data, fetchinfo
from datetime import date

PREFIXES = ["/", "."]

# /start command
@Client.on_message(filters.command("start", prefixes=PREFIXES))
async def start_ui(client, message: Message):
    user_id = str(message.from_user.id)
    username = message.from_user.first_name or "User"

    # Only check, don’t insert here
    reg_data = fetchinfo(user_id)
    status = "✅ Registered" if reg_data else "⚠️ Not Registered"

    await message.reply_text(
        f"⌬ <b>WELCOME TO BARRY BOT</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"• Hello, <b>{username}</b>!\n"
        f"• User ID: <code>{user_id}</code>\n"
        f"• Status: {status}\n"
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

# Register button logic
@Client.on_callback_query(filters.regex("register"))
async def register_btn(client, callback_query: CallbackQuery):
    user_id = str(callback_query.from_user.id)
    username = callback_query.from_user.first_name or "User"
    reg_date = str(date.today())

    if fetchinfo(user_id):
        await callback_query.message.edit_text(
            f"⚠️ Hey <b>{username}</b>, you're already registered in our system!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Back", callback_data="commands")]
            ])
        )
    else:
        insert_reg_data(user_id, username, 200, reg_date)
        await callback_query.message.edit_text(
            f"✅ <b>Registration Successful!</b>\n\n"
            f"• Name: <code>{username}</code>\n"
            f"• User ID: <code>{user_id}</code>\n"
            f"• Plan: FREE\n"
            f"• Credits: 200\n"
            f"• Registered At: <code>{reg_date}</code>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Go to Menu", callback_data="commands")]
            ])
        )

# Command menu
@Client.on_callback_query(filters.regex("commands"))
async def show_command_menu(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "BARRY [COMMAND CENTER]\n━━━━━━━━━━━━━\nSelect a section to explore:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Gate", callback_data="open_gates"),
             InlineKeyboardButton("Tools", callback_data="open_tools")],
            [InlineKeyboardButton("Helper", callback_data="open_helper")],
            [InlineKeyboardButton("Close", callback_data="close_ui")]
        ])
    )

# Close any menu
@Client.on_callback_query(filters.regex("close_ui"))
async def close_menu(client, callback_query):
    await callback_query.message.delete()
