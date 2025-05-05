from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import fetchinfo

@Client.on_message(filters.command("info"))
async def user_info(client: Client, message: Message):
    user_id = message.from_user.id
    user_data = fetchinfo(str(user_id))

    if not user_data:
        await message.reply_text("❌ You are not registered. Please use /register first.", quote=True)
        return

    first_name = message.from_user.first_name or "No Name"
    username = f"@{message.from_user.username}" if message.from_user.username else "N/A"
    profile_link = f"<a href='tg://user?id={user_id}'>Profile Link</a>"

    status = "PREMIUM" if user_data[2].upper() == "PREMIUM" else "FREE"
    plan = user_data[3]
    expiry = user_data[4] if user_data[4] != "N/A" else "Not Set"
    credits = f"{int(user_data[5]):,}"
    keys_used = user_data[10] if len(user_data) > 10 else 0
    reg_date = user_data[9]

    scam = "False"
    premium = "True" if message.from_user.is_premium else "False"
    restricted = "False"

    await message.reply_text(
        f"BARRY | {user_id} Info\n"
        f"━━━━━━━━━━━━━━\n"
        f"[ϟ] First Name : {first_name}\n"
        f"[ϟ] ID : {user_id}\n"
        f"[ϟ] Username : {username}\n"
        f"[ϟ] Profile Link : {profile_link}\n"
        f"[ϟ] TG Restrictions : {restricted}\n"
        f"[ϟ] TG Scamtag : {scam}\n"
        f"[ϟ] TG Premium : {premium}\n"
        f"[ϟ] Status : {status}\n"
        f"[ϟ] Credit : {credits}\n"
        f"[ϟ] Plan : {plan}\n"
        f"[ϟ] Plan Expiry : {expiry}\n"
        f"[ϟ] Keys Redeemed : {keys_used}\n"
        f"[ϟ] Registered At : {reg_date}\n"
        f"━━━━━━━━━━━━━━",
        quote=True,
        
    )
