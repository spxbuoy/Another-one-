from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import fetchinfo

@Client.on_message(filters.command("credits"))
async def check_credits(client: Client, message: Message):
    user_id = message.from_user.id
    user = fetchinfo(str(user_id))

    if not user:
        await message.reply_text("❌ You are not registered. Use /register first.", quote=True)
        return

    name = message.from_user.first_name or "User"
    status = "PREMIUM" if user[2].upper() == "PREMIUM" else "FREE"
    plan = user[3]
    credits = f"{int(user[5]):,}"

    await message.reply_text(
        f"BARRY [CREDIT STATUS]\n"
        f"━━━━━━━━━━━━━━\n"
        f"[ϟ] Name: {name}\n"
        f"[ϟ] Status: {status}\n"
        f"[ϟ] Plan: {plan}\n"
        f"[ϟ] Credits: {credits}\n"
        f"━━━━━━━━━━━━━━\n"
        f"➤ Need more credits? Use /buy",
        quote=True
    )
