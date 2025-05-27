from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import fetchinfo

@Client.on_message(filters.command("credits", prefixes=["/", "."]))
async def check_credits(client: Client, message: Message):
    user_id = str(message.from_user.id)
    user = fetchinfo(user_id)

    if not user:
        return await message.reply_text("❌ You are not registered. Use /register first.", quote=True)

    name = message.from_user.first_name or "User"
    status = user[2].upper() if user[2] else "FREE"
    plan = user[3] or "N/A"
    credits = f"{int(user[5] or 0):,}"

    await message.reply_text(
        f"<b>BARRY [CREDIT STATUS]</b>\n"
        f"<code>━━━━━━━━━━━━━━</code>\n"
        f"➤ <b>Name:</b> {name}\n"
        f"➤ <b>Status:</b> {status}\n"
        f"➤ <b>Plan:</b> {plan}\n"
        f"➤ <b>Credits:</b> {credits}\n"
        f"<code>━━━━━━━━━━━━━━</code>\n"
        f"➤ Need more credits? Use /buy",
        quote=True,
        disable_web_page_preview=True
    )
