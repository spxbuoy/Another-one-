from pyrogram import Client, filters
from plugins.func.users_sql import *

@Client.on_message(filters.command("howcrd"))
async def cmd_howcrd(client, message):
    try:
        user_id = str(message.from_user.id)

        # Credit Info Message
        text = (
            "Barry [CREDIT SYSTEM]\n"
            "━━━━━━━━━━━━━\n"
            "[ϟ] AUTH GATES\n"
            "➤ 1 Credit per CC Check\n"
            "━━━━━━━━━━━━━\n"
            "[ϟ] CHARGE GATES\n"
            "➤ 1 Credit per CC Check\n"
            "━━━━━━━━━━━━━\n"
            "[ϟ] MASS AUTH GATES\n"
            "➤ 1 Credit per CC Check\n"
            "━━━━━━━━━━━━━\n"
            "[ϟ] MASS CHARGE GATES\n"
            "➤ 1 Credit per CC Check\n"
            "━━━━━━━━━━━━━\n"
            "[ϟ] CC SCRAPER GATES\n"
            "➤ 1 Credit per Scraping\n"
            "━━━━━━━━━━━━━"
        )

        await message.reply_text(text, reply_to_message_id=message.id)
        await plan_expirychk(user_id)

    except Exception as e:
        print(f"/howcrd error: {e}")