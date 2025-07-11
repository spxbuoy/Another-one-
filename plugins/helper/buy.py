from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.func.users_sql import plan_expirychk

@Client.on_message(filters.command("buy", prefixes=["/", "."]))
async def cmd_buy(client, message):
    try:
        user_id = str(message.from_user.id)

        linked_ϟ = '<a href="https://t.me/+CUKFuQJYJTUwZmU8">ϟ</a>'

        text = (
            "BARRY [PREMIUM PLANS]\n"
            "━━━━━━━━━━━━━━\n"
            f"[{linked_ϟ}] Starter\n"
            "➤ 2K Credits + 7 Days Premium\n"
            "➤ Price: 3$\n"
            "━━━━━━━━━━━━━━\n"
            f"[{linked_ϟ}] Silver\n"
            "➤ 6K Credits + 15 Days Premium\n"
            "➤ Price: 6.5$\n"
            "━━━━━━━━━━━━━━\n"
            f"[{linked_ϟ}] Gold\n"
            "➤ Unlimited Credits + 1 Month Premium\n"
            "➤ Price: 12$\n"
            "━━━━━━━━━━━━━━\n"
            f"[{linked_ϟ}] Payment Methods:\n"
            "➤ BTC, LTC, USDT\n"
            "━━━━━━━━━━━━━━\n"
            "All plans are valid & Suitable.\n"
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
