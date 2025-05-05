from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import fetchinfo, updatedata
from plugins.admin.gc.gc_func import getgc, updategc
from datetime import date, timedelta
import re

@Client.on_message(filters.command("redeem"))
async def redeem_code(client, message: Message):
    try:
        user_id = message.from_user.id
        args = message.text.split()
        if len(args) != 2:
            return await message.reply_text("⚠️ Usage: <code>/redeem YOUR-CODE</code>", quote=True)

        code = args[1].strip().upper()

        user_info = fetchinfo(user_id)
        if not user_info:
            return await message.reply_text("❌ You are not registered. Please use /register first.")

        row = getgc(code)
        if not row or row[1].upper() != "ACTIVE":
            return await message.reply_text("❌ Invalid or already used code.")

        plan_text = row[2]
        credits = int(row[3])

        # First try using 'days' column from DB (row[4])
        try:
            days = int(row[4])
        except:
            # If missing, fallback to plan name
            fallback_days = {
                "starter": 7,
                "silver": 15,
                "gold": 30
            }
            lower_plan = plan_text.lower()
            days = fallback_days.get(lower_plan)

            if not days:
                return await message.reply_text("❌ Unknown plan format and no fallback found.")

        # Apply gift code
        updategc(code)
        updatedata(user_id, "credits", int(user_info[5] or 0) + credits)
        updatedata(user_id, "plan", plan_text)
        updatedata(user_id, "expiry", str(date.today() + timedelta(days=days)))
        updatedata(user_id, "status", "PREMIUM")

        try:
            total_keys = int(user_info[10]) if user_info[10] else 0
            updatedata(user_id, "totalkey", total_keys + 1)
        except:
            pass

        await message.reply_text(
            f"✅ Successfully redeemed <code>{code}</code>\n"
            f"⭐ Plan upgraded to: <b>{plan_text}</b>\n"
            f"➕ {credits} Credits added!\n"
            f"🗓️ Valid for {days} Days",
            quote=True
        )

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}", quote=True)
