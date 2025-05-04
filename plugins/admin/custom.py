from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import updatedata

CEO_ID = 6440962840  # Owner ID as integer

@Client.on_message(filters.command("cs"))
async def cmd_cs(client: Client, message: Message):
    if message.from_user.id != CEO_ID:
        await message.reply_text("❌ Requires Owner Privileges.", quote=True)
        return

    try:
        _, userid, module_name, value = message.text.split(maxsplit=3)
    except ValueError:
        await message.reply_text(
            "Usage:\n/cs userid modulename value",
            quote=True
        )
        return

    try:
        updatedata(userid, module_name, value)
        resp = (
            "OxEnv [SET USER DATA]\n"
            "━━━━━━━━━━━━━\n"
            f"[ϟ] User ID: {userid}\n"
            f"[ϟ] Module: {module_name}\n"
            f"[ϟ] New Value: {value}\n"
            "━━━━━━━━━━━━━\n"
            "Successfully Updated ✅"
        )
        await message.reply_text(resp, quote=True)

    except Exception as e:
        await message.reply_text(f"Error:\n<code>{e}</code>",  quote=True)