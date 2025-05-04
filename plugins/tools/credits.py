from pyrogram import Client, filters
from plugins.func.users_sql import *

@Client.on_message(filters.command("credits"))
async def cmd_credit(client, message):
    try:
        user_id = str(message.from_user.id)
        regdata = fetchinfo(user_id)
        first_name = message.from_user.first_name or "User"

        if regdata is None:
            await message.reply_text(
                "⚠️ You are not registered yet.\nUse /register to get started.",
                reply_to_message_id=message.id
            )
            return

        credit = regdata[5]
        status = regdata[2]
        plan = regdata[3]

        text = (
            "OxEnv [CREDIT STATUS]\n"
            "━━━━━━━━━━━━━━\n"
            f"[ϟ] Name: {first_name}\n"
            f"[ϟ] Status: {status}\n"
            f"[ϟ] Plan: {plan}\n"
            f"[ϟ] Credits: {credit}\n"
            "━━━━━━━━━━━━━━\n"
            "➤ Need more credits? Use /buy"
        )

        await message.reply_text(text, reply_to_message_id=message.id)
        await plan_expirychk(user_id)

    except Exception as e:
        print(f"[ERROR /credits]: {e}")