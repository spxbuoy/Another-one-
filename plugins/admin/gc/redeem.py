from plugins.admin.gc.gc_func import getgc, updategc
from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import fetchinfo, updatedata
from datetime import date, timedelta

@Client.on_message(filters.command("redeem"))
async def cmd_gc(client: Client, message: Message):
    try:
        user_id = str(message.from_user.id)
        user_data = fetchinfo(user_id)

        if not user_data:
            await message.reply_text(
                "❌ You are not registered yet.\nUse <code>/register</code> first.",
                quote=True
            )
            return

        try:
            gift_code = message.text.split(maxsplit=1)[1].strip()
        except IndexError:
            await message.reply_text("⚠️ Usage: <code>/redeem YOUR_GIFTCODE</code>", quote=True)
            return

        code_data = getgc(gift_code)
        if not code_data:
            await message.reply_text("❌ Invalid Giftcode.", quote=True)
            return

        status, plan = code_data[1], code_data[2]
        if status != "ACTIVE":
            await message.reply_text("⚠️ This Giftcode has already been used.", quote=True)
            return

        # Handle dynamic days like PREMIUM_7 or PREMIUM_365
        if plan.startswith("PREMIUM_"):
            days = int(plan.split("_")[1])
            plan_name = f"Premium Plan ({days} Days)"
            credits = 5000
            expiry = date.today() + timedelta(days=days)
        else:
            plan_map = {
                "PREMIUM": {"credits": 100, "expiry": 0, "plan": None},
                "PLAN1": {"credits": 1000, "expiry": 7, "plan": "Starter Plan 0.99$"},
                "PLAN2": {"credits": 2000, "expiry": 15, "plan": "Silver Plan 1.99$"},
                "PLAN3": {"credits": 5000, "expiry": 30, "plan": "Gold Plan 4.99$"},
            }
            if plan not in plan_map:
                await message.reply_text("❌ Unknown plan type in giftcode.", quote=True)
                return
            plan_info = plan_map[plan]
            plan_name = plan_info["plan"] or "Premium Access"
            credits = plan_info["credits"]
            expiry = date.today() + timedelta(days=plan_info["expiry"]) if plan_info["expiry"] else None

        updatedata(user_id, "totalkey", int(user_data[8]) + 1)
        updatedata(user_id, "credit", int(user_data[5]) + credits)
        updatedata(user_id, "status", "PREMIUM")
        if plan_name:
            updatedata(user_id, "plan", plan_name)
        if expiry:
            updatedata(user_id, "expiry", str(expiry))

        updategc(gift_code)

        msg = (
            f"BARRY [REDEEMED]\n"
            f"━━━━━━━━━━━━━\n"
            f"[ϟ] Giftcode: <code>{gift_code}</code>\n"
            f"[ϟ] Plan: <b>{plan_name}</b>\n"
            f"[ϟ] Credit: {credits}\n"
            f"[ϟ] Status: <b>Activated ✅</b>\n"
            f"━━━━━━━━━━━━━\n"
            f"<b>Use</b> <code>/info</code> to view your account details."
        )
        await message.reply_text(msg, quote=True)

    except Exception as e:
        await message.reply_text(f"❌ Error: <code>{e}</code>", quote=True)