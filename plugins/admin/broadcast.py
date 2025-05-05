from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import getalldata

CEO_ID = 6440962840  # Replace with your actual Telegram user ID

@Client.on_message(filters.command("br"))
async def cmd_br(client: Client, message: Message):
    if message.from_user.id != CEO_ID:
        await message.reply_text("❌ Access Denied\nOnly the bot owner can use this command.", quote=True)
        return

    broadcast_text = "Hi All — This is a test broadcast from OxEnv."
    filter_user = "users"

    try:
        users = getalldata(filter_user)
        count = 0
        for user in users:
            chat_id = int(user[0])
            try:
                await client.send_message(chat_id, broadcast_text)
                count += 1
            except Exception as e:
                print(f"[Failed] {chat_id}: {e}")
                continue

        await message.reply_text(
            f"BARRY [BROADCAST DONE]\n"
            f"━━━━━━━━━━━━━\n"
            f"[ϟ] Total Users Reached: {count}\n"
            f"━━━━━━━━━━━━━",
            quote=True
        )
    except Exception as e:
        await client.send_message(CEO_ID, f"❌ Broadcast Error: {e}")