import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.func.utils import error_log  # Make sure this function exists


@Client.on_message(filters.command("ping", [".", "/"]))
async def cmd_ping(client, message):
    try:
        start = time.perf_counter()
        checking_msg = await message.reply_text("⏳ Checking Ping...", quote=True)
        end = time.perf_counter()
        ping_ms = (end - start) * 1000

        response = f"""<b>[⚡] BARRY Ping Panel</b>
━━━━━━━━━━━━━━━━━━
[⚙️] Bot Name: <code>BARRY Checker</code>
[✅] Status: <code>UP & Running</code>
[📶] Ping: <code>{ping_ms:.2f} ms</code>
━━━━━━━━━━━━━━━━━━"""

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Refresh Ping", callback_data="refresh_ping")],
            [InlineKeyboardButton("Back to Commands", callback_data="commands")]
        ])

        await client.edit_message_text(
            chat_id=message.chat.id,
            message_id=checking_msg.id,
            text=response,
            reply_markup=buttons
        )

    except Exception as e:
        await error_log(str(e))


@Client.on_callback_query(filters.regex("refresh_ping"))
async def refresh_ping_cb(client, callback_query):
    try:
        start = time.perf_counter()
        await callback_query.answer("Refreshing ping...", show_alert=False)
        end = time.perf_counter()
        ping_ms = (end - start) * 1000

        response = f"""<b>[⚡] BARRY Ping Panel</b>
━━━━━━━━━━━━━━━━━━
[⚙️] Bot Name: <code>BARRY Checker</code>
[✅] Status: <code>UP & Running</code>
[📶] Ping: <code>{ping_ms:.2f} ms</code>
━━━━━━━━━━━━━━━━━━"""

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Refresh Ping", callback_data="refresh_ping")],
            [InlineKeyboardButton("Back to Commands", callback_data="commands")]
        ])

        await callback_query.message.edit_text(response, reply_markup=buttons)

    except Exception as e:
        await error_log(str(e))