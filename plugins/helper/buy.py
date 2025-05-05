from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.func.users_sql import plan_expirychk

@Client.on_message(filters.command("buy"))
async def cmd_buy(client, message):
    try:
        user_id = str(message.from_user.id)

        text = (
            "BARRY [PREMIUM PLANS]\n"
            "━━━━━━━━━━━━━━\n"
            "[ϟ] Starter\n"
            "➤ 1K Credits + 7 Days Premium\n"
            "➤ Price: 0.99$\n"
            "━━━━━━━━━━━━━━\n"
            "[ϟ] Silver\n"
            "➤ 2K Credits + 15 Days Premium\n"
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
            "You must repurchase to continue using premium after expiry."
        )

        await message.reply_text(
            text,
            reply_to_message_id=message.id,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("CLICK HERE TO BUY PLAN", url="https://t.me/Barry_op")]]
            )
        )

        plan_expirychk(user_id)

    except Exception as e:
        print(f"[ERROR /buy]: {e}")