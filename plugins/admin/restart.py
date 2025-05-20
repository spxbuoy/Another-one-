import os
import sys
import traceback
from pyrogram import Client, filters

OWNER_IDS = ["6440962840"]

async def error_log(error_text):
    with open("error.log", "a", encoding="utf-8") as f:
        f.write(f"\n{'='*30}\n{error_text}\n")

@Client.on_message(filters.command("reload", prefixes=["/", "."]))
async def cmd_reboot(client, message):
    try:
        user_id = str(message.from_user.id)

        if user_id not in OWNER_IDS:
            return await message.reply_text(
                "<b>⚠️ Privilege Denied</b>\n"
                "You are not authorized to perform this action.\n"
                "Contact @Barry_op for access."
            )

        await message.reply_text("♻️ <b>Reloading bot... Please wait.</b>")

        # Restart the Python bot process
        os.execv(sys.executable, [sys.executable] + sys.argv)

    except Exception as e:
        await message.reply_text(f"❌ Error occurred:\n<code>{str(e)}</code>")
        await error_log(traceback.format_exc())