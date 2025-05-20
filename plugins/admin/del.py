from pyrogram import Client, filters
from pyrogram.types import Message

CEO_ID = 6440962840  # Your hardcoded owner ID
GROUP_FILE = "plugins/group.txt"

@Client.on_message(filters.command("del", prefixes=["/", "."]))
async def cmd_del(client: Client, message: Message):
    user_id = message.from_user.id

    if user_id != CEO_ID:
        await message.reply_text("𝗥𝗲𝗾𝘂𝗶𝗿𝗲 𝗢𝘄𝗻𝗲𝗿 𝗣𝗿𝗶𝘃𝗶𝗹𝗲𝗴𝗲𝘀 ⚠️", quote=True)
        return

    # Get chat_id from message or fallback to current chat
    try:
        chat_del = message.text.split(maxsplit=1)[1]
    except IndexError:
        chat_del = str(message.chat.id)

    group_id = chat_del.strip()

    # Read current list
    try:
        with open(GROUP_FILE, "r") as f:
            group_ids = f.read().splitlines()
    except FileNotFoundError:
        group_ids = []

    if group_id not in group_ids:
        await message.reply_text(
            f"𝗧𝗵𝗶𝘀 𝗴𝗿𝗼𝘂𝗽 (<code>{group_id}</code>) 𝗶𝘀 𝗻𝗼𝘁 𝗶𝗻 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗹𝗶𝘀𝘁 ⚠️.",
            quote=True
        )
    else:
        group_ids.remove(group_id)
        with open(GROUP_FILE, "w") as f:
            f.write("\n".join(group_ids) + "\n")
        await message.reply_text(
            f"𝗧𝗵𝗶𝘀 𝗴𝗿𝗼𝘂𝗽 (<code>{group_id}</code>) 𝗶𝘀 𝗱𝗲𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 ❌.",
            quote=True
        )

        # Optional: notify the group if still in it
        try:
            await client.send_message(group_id, "𝗧𝗵𝗶𝘀 𝗴𝗿𝗼𝘂𝗽 𝗶𝘀 𝗻𝗼 𝗹𝗼𝗻𝗴𝗲𝗿 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗲 𝗯𝗼𝘁.")
        except:
            pass