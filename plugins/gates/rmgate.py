from pyrogram import Client, filters
from plugins.func.users_sql import remove_user_gate

@Client.on_message(filters.command("rmgate", ["/", "."]))
async def delete_user_gate(client, message):
    try:
        user_id = str(message.from_user.id)
        remove_user_gate(user_id)
        await message.reply_text("✅ Your gate has been removed.", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error removing gate:\n<code>{str(e)}</code>", quote=True)