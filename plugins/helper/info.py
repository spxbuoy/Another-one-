from pyrogram import Client, filters
from plugins.func.users_sql import *

@Client.on_message(filters.command("info"))
async def cmd_info(client, message):
    try:
        target_user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
        user_id = str(target_user.id)
        first_name = target_user.first_name or "User"
        username = target_user.username or "N/A"
        is_restricted = target_user.is_restricted
        is_scam = target_user.is_scam
        is_premium = target_user.is_premium

        info = fetchinfo(user_id)

        # Plan check
        await plan_expirychk(user_id)

        if info is None:
            send_info = f"""
𝗬𝗼𝘂𝗿 𝗜𝗻𝗳𝗼 𝗼𝗻 𝗕𝗔𝗥𝗥𝗬 𝗖𝗖 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 ⚡
━━━━━━━━━━━━━━
● 𝗙𝗶𝗿𝘀𝘁𝗻𝗮𝗺𝗲: {first_name}
● 𝗜𝗗: <code>{user_id}</code>
● 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: {username}
● 𝗣𝗿𝗼𝗳𝗶𝗹𝗲 𝗟𝗶𝗻𝗸: <a href="tg://user?id={user_id}">Profile Link</a>
● 𝗧𝗚 𝗥𝗲𝘀𝘁𝗿𝗶𝗰𝘁𝗶𝗼𝗻𝘀: {is_restricted}
● 𝗧𝗚 𝗦𝗰𝗮𝗺𝘁𝗮𝗴: {is_scam}
● 𝗧𝗚 𝗣𝗿𝗲𝗺𝗶𝘂𝗺: {is_premium}
● 𝗦𝘁𝗮𝘁𝘂𝘀: NOT REGISTERED
● 𝗖𝗿𝗲𝗱𝗶𝘁: N/A
● 𝗣𝗹𝗮𝗻: N/A
● 𝗣𝗹𝗮𝗻 𝗘𝘅𝗽𝗶𝗿𝘆: N/A
● 𝗞𝗲𝘆 𝗥𝗲𝗱𝗲𝗲𝗺𝗲𝗱: N/A
● 𝗥𝗲𝗴𝗶𝘀𝘁𝗲𝗿𝗲𝗱 𝗮𝘁: N/A
"""
        else:
            status = info[2]
            plan = info[3]
            expiry = info[4]
            credit = info[5]
            totalkey = info[8]
            reg_at = info[9]

            send_info = f"""
𝗬𝗼𝘂𝗿 𝗜𝗻𝗳𝗼 𝗼𝗻 𝗕𝗔𝗥𝗥𝗬 𝗖𝗖 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 ⚡
━━━━━━━━━━━━━━
● 𝗙𝗶𝗿𝘀𝘁𝗻𝗮𝗺𝗲: {first_name}
● 𝗜𝗗: <code>{user_id}</code>
● 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: {username}
● 𝗣𝗿𝗼𝗳𝗶𝗹𝗲 𝗟𝗶𝗻𝗸: <a href="tg://user?id={user_id}">Profile Link</a>
● 𝗧𝗚 𝗥𝗲𝘀𝘁𝗿𝗶𝗰𝘁𝗶𝗼𝗻𝘀: {is_restricted}
● 𝗧𝗚 𝗦𝗰𝗮𝗺𝘁𝗮𝗴: {is_scam}
● 𝗧𝗚 𝗣𝗿𝗲𝗺𝗶𝘂𝗺: {is_premium}
● 𝗦𝘁𝗮𝘁𝘂𝘀: {status}
● 𝗖𝗿𝗲𝗱𝗶𝘁: {credit}
● 𝗣𝗹𝗮𝗻: {plan}
● 𝗣𝗹𝗮𝗻 𝗘𝘅𝗽𝗶𝗿𝘆: {expiry}
● 𝗞𝗲𝘆 𝗥𝗲𝗱𝗲𝗲𝗺𝗲𝗱: {totalkey}
● 𝗥𝗲𝗴𝗶𝘀𝘁𝗲𝗿𝗲𝗱 𝗮𝘁: {reg_at}
"""

        await message.reply_text(send_info, reply_to_message_id=message.id)

    except Exception as e:
        print(f"[ERROR /info]: {e}")
        