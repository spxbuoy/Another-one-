from pyrogram import Client, filters
from plugins.func.users_sql import *

@Client.on_message(filters.command("buy"))
async def cmd_buy(client, message):
    try:
        user_id = str(message.from_user.id)

        text = (
            "BARRY [PREMIUM PLANS]\n"
            "━━━━━━━━━━━━━━\n"
            "[ϟ] Starter\n"
            "➤ 1K Credits + 1 Month Premium\n"
            "➤ Price: 0.99$\n"
            "━━━━━━━━━━━━━━\n"
            "[ϟ] Silver\n"
            "➤ 2K Credits + 1 Month Premium\n"
            "➤ Price: 1.99$\n"
            "━━━━━━━━━━━━━━\n"
            "[ϟ] Gold\n"
            "➤ 5K Credits + 1 Month Premium\n"
            "➤ Price: 4.99$\n"
            "━━━━━━━━━━━━━━\n"
            "[ϟ] Payment Methods:\n"
            "➤ BTC, LTC, USDT\n"
            "━━━━━━━━━━━━━━\n"
            "All plans are valid for 1 month.\n"
            "You must repurchase to continue using premium after expiry.\n"
            "━━━━━━━━━━━━━━\n"
         "<a href='tg://user?id=6440962840'>CLICK HERE TO BUY PLAN</a>"
        )

        await message.reply_text(text, reply_to_message_id=message.id,  disable_web_page_preview=True)
        await plan_expirychk(user_id)

    except Exception as e:
        print(f"[ERROR /buy]: {e}")