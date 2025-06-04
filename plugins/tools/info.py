from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import fetchinfo

@Client.on_message(filters.command("info", prefixes=["/", "."]))
async def user_info(client: Client, message: Message):
    target_user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    user_id = str(target_user.id)

    user_data = fetchinfo(user_id)
    if not user_data:
        return await message.reply_text("❌ User is not registered in the database.", quote=True)

    linked_ϟ = '<a href="https://t.me/+CUKFuQJYJTUwZmU8">ϟ</a>'

    first_name = target_user.first_name or "No Name"
    username = f"@{target_user.username}" if target_user.username else "N/A"
    profile_link = f"<a href='tg://user?id={user_id}'>Profile Link</a>"

    status = user_data[2].upper() if user_data[2] else "FREE"
    plan = user_data[3] if user_data[3] and user_data[3] != "None" else "N/A"
    expiry = user_data[4] if user_data[4] and user_data[4] != "None" else "N/A"
    credits = f"{int(user_data[5]):,}" if user_data[5] else "0"
    reg_date = user_data[9] if user_data[9] else "Unknown"
    keys_used = user_data[10] if len(user_data) > 10 and user_data[10] else 0

    scam = "False"
    premium = "True" if getattr(target_user, "is_premium", False) else "False"
    restricted = "False"

    text = f"""
<b>BARRY | {user_id} Info</b>
<code>━━━━━━━━━━━━━━</code>
<b>[{linked_ϟ}] First Name :</b> {first_name}
<b>[{linked_ϟ}] ID :</b> {user_id}
<b>[{linked_ϟ}] Username :</b> {username}
<b>[{linked_ϟ}] Profile Link :</b> {profile_link}
<b>[{linked_ϟ}] TG Restrictions :</b> {restricted}
<b>[{linked_ϟ}] TG Scamtag :</b> {scam}
<b>[{linked_ϟ}] TG Premium :</b> {premium}
<b>[{linked_ϟ}] Status :</b> {status}
<b>[{linked_ϟ}] Credit :</b> {credits}
<b>[{linked_ϟ}] Plan :</b> {plan}
<b>[{linked_ϟ}] Plan Expiry :</b> {expiry}
<b>[{linked_ϟ}] Keys Redeemed :</b> {keys_used}
<b>[{linked_ϟ}] Registered At :</b> {reg_date}
<code>━━━━━━━━━━━━━━</code>
"""

    try:
        await message.reply_text(text, quote=True, disable_web_page_preview=True)
    except Exception:
        fallback_link = f"tg://user?id={user_id}"
        await message.reply_text(
            text.replace(profile_link, fallback_link),
            quote=True,
            disable_web_page_preview=True
        )
