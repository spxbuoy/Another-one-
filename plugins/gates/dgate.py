from pyrogram import Client, filters
from plugins.func.users_sql import delete_custom_gate

@Client.on_message((filters.command("dgate") | filters.regex(r"^\.dgate")) & filters.private)
async def dgate(client, message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            return await message.reply("❌ Usage: /dgate /yourcommand")

        command = parts[1].strip()
        #if not command.startswith("/"):
#            command = "/" + command

        delete_custom_gate(message.from_user.id, command)
        await message.reply(f"✅ Gate {command} removed.")

    except Exception as e:
        await message.reply(f"❌ Error removing gate:\n{e}")
