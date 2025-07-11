from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import fetchinfo, updatedata
from datetime import date, timedelta
import random, string

CEO_ID = 6440962840  # Your Telegram ID

def generate_txid():
    return "BOA-TX" + ''.join(random.choices(string.digits, k=7))

@Client.on_message(filters.command("subs", prefixes=["/", "."]))
async def manual_subs_cmd(client: Client, message: Message):
    if message.from_user.id != CEO_ID:
        await message.reply_text("⛔ <b>Owner privileges required.</b>", quote=True)
        return

    args = message.command
    if len(args) < 3:
        await message.reply_text("⚠️ <b>Usage:</b> <code>/subs user_id payment_method</code>", quote=True)
        return

    _, userid, payment_method = args

    try:
        user_data = fetchinfo(userid)
        if not user_data:
            await message.reply_text("⚠️ <b>User is not registered to the bot.</b>", quote=True)
            return

        # Upgrade logic
        updatedata(userid, "plan", "STARTER")
        updatedata(userid, "credits", int(user_data[5]) + 2000)
        updatedata(userid, "expiry", str(date.today() + timedelta(days=7)))
        updatedata(userid, "status", "PREMIUM")
        updatedata(userid, "totalkey", 0)

        # Admin UI message
        plan_ui = (
            "╭━━━〔 𝙋𝙇𝘼𝙉 𝙐𝙋𝙂𝙍𝘼𝘿𝙀 〕━━━╮\n"
            f"┣➤ 👤 User       : <a href='tg://user?id={userid}'>{userid}</a>\n"
            f"┣➤ 🧾 Plan       : <b>Starter Plan 3$</b>\n"
            f"┣➤ 💳 Price      : <b>3$</b>\n"
            f"┣➤ ⭐ Status     : <b>PREMIUM ✅</b>\n"
            f"┣➤ 🏦 Method     : <b>{payment_method}</b>\n"
            f"┣➤ 📅 Upgraded   : <b>{str(date.today())}</b>\n"
            "╰━━━━━━━━━━━━━━━━━━━━╯"
        )
        await message.reply_text(plan_ui, quote=True)

        # Bank-style receipt to user
        today = str(date.today())
        expiry = str(date.today() + timedelta(days=7))
        txid = generate_txid()
        user_name = message.from_user.first_name or "User"

        receipt = (
            "━━━━━━━━━━━━━\n"
            "[𝑩𝑨𝑵𝑲 𝑻𝑹𝑨𝑵𝑺𝑭𝑬𝑹 𝑹𝑬𝑪𝑬𝑰𝑷𝑻]\n"
            "━━━━━━━━━━━━━\n"
            f"Account Holder : {user_name}\n"
            f"Account ID     : {userid}\n"
            f"Plan           : Starter Plan 3$\n"
            f"Transaction ID : {txid}\n"
            f"Status         : ✅ Settled\n"
            f"Received Via   : {payment_method}\n"
            f"Bank Name      : Barry Intl Ltd.\n"
            f"Date           : {today}\n"
            f"Expiry         : {expiry}\n"
            "━━━━━━━━━━━━━\n"
            "Note: Thank you for using Barry Subscription Services."
        )

        await client.send_message(int(userid), receipt)

    except Exception as e:
        await message.reply_text(f"❌ <b>Error:</b> <code>{e}</code>", quote=True)
