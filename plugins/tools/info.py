from pyrogram import Client, filters
from plugins.func.users_sql import *

@Client.on_message(filters.command("info"))
async def cmd_info(client, message):
    try:
        target_user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
        user_id = str(target_user.id)
        first_name = target_user.first_name or "User"
        username = f"@{target_user.username}" if target_user.username else "N/A"
        is_restricted = target_user.is_restricted
        is_scam = target_user.is_scam
        is_premium = target_user.is_premium

        info = fetchinfo(user_id)
        await plan_expirychk(user_id)

        if info is None:
            status = "NOT REGISTERED"
            credit = "N/A"
            plan = "N/A"
            expiry = "N/A"
            totalkey = "N/A"
            reg_at = "N/A"
        else:
            status = info[2]
            plan = info[3]
            expiry = info[4]
            credit = info[5]
            totalkey = info[8]
            reg_at = info[9]

        send_info = f"""
<b>BARRY | {user_id} Info</b>
━━━━━━━━━━━━━━
[ϟ] First Name : {first_name}
[ϟ] ID : <code>{user_id}</code>
[ϟ] Username : {username}
[ϟ] Profile Link : <a href="tg://user?id={user_id}">Profile Link</a>
[ϟ] TG Restrictions : {is_restricted}
[ϟ] TG Scamtag : {is_scam}
[ϟ] TG Premium : {is_premium}
[ϟ] Status : {status}
[ϟ] Credit : {credit}
[ϟ] Plan : {plan}
[ϟ] Plan Expiry : {expiry}
[ϟ] Keys Redeemed : {totalkey}
[ϟ] Registered At : {reg_at}
━━━━━━━━━━━━━━
"""

        await message.reply_text(send_info, reply_to_message_id=message.id)

    except Exception as e:
        await message.reply_text(f"⚠️ <b>Error:</b> <code>{str(e)}</code>")