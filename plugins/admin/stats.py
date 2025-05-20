from pyrogram import Client, filters
from plugins.func.users_sql import get_user_stats, getalldata

OWNER_ID = "6440962840"

@Client.on_message(filters.command("stats", [".", "/"]))
async def stats_cmd(Client, message):
    try:
        user_id = str(message.from_user.id)

        if user_id != OWNER_ID:
            return await message.reply_text("<b>╰┈➤ You are not the owner!</b>", message.id)

        total_users, premium_users = get_user_stats()
        all_users = getalldata()

        free_users = 0
        paid_users = 0
        starter_users = 0
        silver_users = 0
        gold_users = 0

        for user in all_users:
            status = user[2]
            plan = user[3]

            if status == "FREE":
                free_users += 1
            elif status == "PREMIUM":
                paid_users += 1

            if plan == "STARTER":
                starter_users += 1
            elif plan == "SILVER":
                silver_users += 1
            elif plan == "GOLD":
                gold_users += 1

        text = f"""
<b>┏━━━━━━━⍟</b>
<b>┃ STATS GATE</b>
<b>┗━━━━━━━━━━━⊛</b>
<b>• Database:</b> <code>SQLite</code>

<b>• Registered Users:</b> <code>{total_users}</code>
<b>• Free Users:</b> <code>{free_users}</code>
<b>• Premium Users:</b> <code>{premium_users}</code>
<b>• Starter Users:</b> <code>{starter_users}</code>
<b>• Silver Users:</b> <code>{silver_users}</code>
<b>• Gold Users:</b> <code>{gold_users}</code>
<b>• Active User Ratio:</b> <code>{premium_users * 3}</code>

<b>• Status:</b> <code>Running</code>
<b>• Checked On:</b> <code>{message.date}</code>
"""
        await message.reply_text(text, message.id)

    except Exception as e:
        await message.reply_text(f"<b>❌ Error:</b> <code>{e}</code>")
