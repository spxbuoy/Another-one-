from pyrogram import Client, filters
from plugins.func.users_sql import getalldata
from datetime import datetime

OWNER_ID = "6440962840"

@Client.on_message(filters.command("stats", [".", "/"]))
async def stats_cmd(Client, message):
    try:
        user_id = str(message.from_user.id)
        if user_id != OWNER_ID:
            return await message.reply_text("<b>╰┈➤ You are not the owner!</b>", message.id)

        all_users = getalldata()

        total_users = len(all_users)
        free_users = 0
        premium_users = 0
        manual_premium = 0
        redeemed_premium = 0
        starter_users = 0
        silver_users = 0
        gold_users = 0

        for user in all_users:
            status = user[2]
            plan = user[3]
            totalkey = int(user[10] or 0)

            if status == "FREE":
                free_users += 1
            elif status == "PREMIUM":
                premium_users += 1
                if totalkey > 0:
                    redeemed_premium += 1
                else:
                    manual_premium += 1

            if plan == "STARTER":
                starter_users += 1
            elif plan == "SILVER":
                silver_users += 1
            elif plan == "GOLD":
                gold_users += 1

        checked_on = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        text = f"""
<b>┏━━━━━━━⍟</b>
<b>┃ 𝗕𝗢𝗧 𝗨𝗦𝗘𝗥 𝗦𝗧𝗔𝗧𝗦</b>
<b>┗━━━━━━━━━━━⊛</b>

<b>• Database:</b> <code>SQLite</code>
<b>• Total Users:</b> <code>{total_users}</code>
<b>• Free Users:</b> <code>{free_users}</code>
<b>• Premium Users:</b> <code>{premium_users}</code>
<b>    ├─ Manual Premium:</b> <code>{manual_premium}</code>
<b>    └─ Redeemed Code:</b> <code>{redeemed_premium}</code>

<b>• Starter Plan:</b> <code>{starter_users}</code>
<b>• Silver Plan:</b> <code>{silver_users}</code>
<b>• Gold Plan:</b> <code>{gold_users}</code>

<b>• Status:</b> <code>Online</code>
<b>• Checked On:</b> <code>{checked_on}</code>
"""
        await message.reply_text(text.strip(), message.id)

    except Exception as e:
        await message.reply_text(f"<b>❌ Error:</b> <code>{e}</code>")