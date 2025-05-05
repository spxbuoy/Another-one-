from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import fetchinfo, updatedata
from plugins.admin.gc.gc_func import getgc, updategc
from datetime import date, timedelta

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
        if not row or row[1] != "ACTIVE":
            return await message.reply_text("❌ Invalid or already used code.")

        plan = row[2]
        credits_map = {
            "Starter": 500,
            "Silver": 5000,
            "Gold": 20000,
        }
        days_map = {
            "Starter": 7,
            "Silver": 15,
            "Gold": 30,
        }

        matched_plan = None
        for p in credits_map:
            if p.lower() in plan.lower():
                matched_plan = p
                break

        if not matched_plan:
            return await message.reply_text("❌ Unknown plan type in the code.")

        credits = credits_map[matched_plan]
        days = days_map[matched_plan]

        # Update DB
        updategc(code)
        updatedata(user_id, "credits", int(user_info[5]) + credits)
        updatedata(user_id, "plan", matched_plan)
        updatedata(user_id, "expiry", str(date.today() + timedelta(days=days)))
        updatedata(user_id, "status", "PREMIUM")

        try:
            total_keys = int(user_info[10]) if user_info[10] else 0
            updatedata(user_id, "totalkey", total_keys + 1)
        except:
            pass

        await message.reply_text(
            f"✅ Successfully redeemed <code>{code}</code>\n"
            f"⭐ Plan upgraded to: <b>{matched_plan}</b>\n"
            f"➕ {credits} Credits added!\n"
            f"🗓️ Valid for {days} Days",
            quote=True
        )

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}", quote=True)