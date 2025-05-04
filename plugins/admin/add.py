from pyrogram import Client, filters
from pyrogram.types import Message

CEO_ID = 6440962840  # Use as integer, not string
GROUP_FILE = "plugins/group.txt"

@Client.on_message(filters.command("add"))
async def cmd_add(client: Client, message: Message):
    user_id = message.from_user.id

    if user_id != CEO_ID:
        await message.reply_text("𝗥𝗲𝗾𝘂𝗶𝗿𝗲 𝗢𝘄𝗻𝗲𝗿 𝗣𝗿𝗶𝘃𝗶𝗹𝗲𝗴𝗲𝘀 ⚠️", quote=True)
        return

    # Get chat_id from message or fallback to current chat
    try:
        chat_add = message.text.split(maxsplit=1)[1]
    except IndexError:
        chat_add = str(message.chat.id)

    group_id = chat_add.strip()

    # Read existing group IDs
    try:
        with open(GROUP_FILE, "r") as f:
            group_ids = f.read().splitlines()
    except FileNotFoundError:
        group_ids = []

    # Check if already added
    if group_id in group_ids:
        await message.reply_text(
            f"𝗧𝗵𝗶𝘀 𝗴𝗿𝗼𝘂𝗽 (<code>{group_id}</code>) 𝗶𝘀 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 ⚠️.",
            quote=True
        )
    else:
        with open(GROUP_FILE, "a") as f:
            f.write(f"{group_id}\n")
        await message.reply_text(
            f"𝗧𝗵𝗶𝘀 𝗴𝗿𝗼𝘂𝗽 (<code>{group_id}</code>) 𝗶𝘀 𝗻𝗼𝘄 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 ✅.",
            quote=True
        )