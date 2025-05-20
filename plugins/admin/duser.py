from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import delete_user
from plugins.func.utils import error_log
import traceback

CEO_ID = 6440962840  # Replace with your actual Telegram ID

@Client.on_message(filters.command("duser", prefixes=["/", "."]))
async def cmd_deluser(client: Client, message: Message):
    try:
        user_id = message.from_user.id

        if user_id != CEO_ID:
            await message.reply_text(
                "╰┈➤ 𝗬𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝘁𝗵𝗲 𝗢𝘄𝗻𝗲𝗿 ⚠️", quote=True
            )
            return

        # Get target user ID
        try:
            if message.reply_to_message:
                target_id = str(message.reply_to_message.from_user.id)
            else:
                target_id = str(message.text.split(maxsplit=1)[1])
        except:
            await message.reply_text(
                "<b>⚠️ Invalid ID!\nReply to a user or provide a valid ID to delete.</b>",
                quote=True
            )
            return

        # Run delete without await
        delete_user(target_id)

        # Styled UI response
        await message.reply_text(
            f"𝗨𝘀𝗲𝗿 𝗥𝗲𝗺𝗼𝘃𝗲𝗱 𝗳𝗿𝗼𝗺 𝗗𝗮𝘁𝗮𝗯𝗮𝘀𝗲 ✅\n"
            f"━━━━━━━━━━━━━━━\n"
            f"[ϟ] User ID : <code>{target_id}</code>\n"
            f"[ϟ] Message : <i>User has been removed from the database.</i>",
            quote=True
        )

    except Exception:
        await error_log(traceback.format_exc())