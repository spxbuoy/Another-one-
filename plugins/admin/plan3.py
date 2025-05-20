from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import fetchinfo, updatedata
from datetime import date, timedelta
from plugins.func.utils import randgen  # Make sure this exists

CEO_ID = 6440962840  # Owner's Telegram ID

@Client.on_message(filters.command("sub3", prefixes=["/", "."]))
async def cmd_sub3(client: Client, message: Message):
    if message.from_user.id != CEO_ID:
        await message.reply_text("⛔ <b>Owner privileges required.</b>", quote=True, )
        return

    try:
        _, userid, payment_method = message.text.split(maxsplit=2)
        user_data = fetchinfo(userid)

        if not user_data:
            await message.reply_text("⚠️ <b>User is not registered to the bot.</b>", quote=True, )
            return

        # Update user
        updatedata(userid, "plan", "Gold Plan 4.99$")
        updatedata(userid, "credit", int(user_data[5]) + 5000)
        expiry = str(date.today() + timedelta(days=30))
        updatedata(userid, "expiry", expiry)
        updatedata(userid, "status", "PREMIUM")

        today = str(date.today())
        receipt_id = randgen(len=10)

        # Admin reply
        await message.reply_text(
            "Barry [PLAN UPGRADE]\n"
            "━━━━━━━━━━━━━\n"
            f"[ϟ] User: <a href='tg://user?id={userid}'>{userid}</a>\n"
            f"[ϟ] Plan: <b>Gold</b>\n"
            f"[ϟ] Price: <b>4.99$</b>\n"
            f"[ϟ] Status: <b>PREMIUM ✅</b>\n"
            "━━━━━━━━━━━━━",
            
            quote=True
        )

        # User receipt message
        user_msg = (
            "Barry [RECEIPT]\n"
            "━━━━━━━━━━━━━\n"
            f"[ϟ] Plan: <b>Gold</b>\n"
            f"[ϟ] Price: <b>4.99$</b>\n"
            f"[ϟ] Purchase Date: <b>{today}</b>\n"
            f"[ϟ] Expiry Date: <b>{expiry}</b>\n"
            f"[ϟ] Status: <b>Paid ☑️</b>\n"
            f"[ϟ] Payment Method: <b>{payment_method}</b>\n"
            f"[ϟ] Receipt ID: <b>BarryCC{receipt_id}</b>\n"
            "━━━━━━━━━━━━━\n"
            "💡 Use <code>/credits</code> to check your balance."
        )

        await client.send_message(int(userid), user_msg, )

    except ValueError:
        await message.reply_text("⚠️ <b>Usage:</b> <code>/sub3 user_id payment_method</code>", quote=True, )
    except Exception as e:
        await message.reply_text(f"❌ <b>Error:</b> <code>{e}</code>", quote=True, )