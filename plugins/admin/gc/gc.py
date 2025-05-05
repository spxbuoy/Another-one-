from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.admin.gc.gc_func import gcgenfunc, insert_giftcode

@Client.on_message(filters.command("gc"))
async def generate_gc(client: Client, message: Message):
    if message.from_user.id != 6440962840:
        return await message.reply_text("⚠️ Owner only command")

    try:
        args = message.text.split()
        count = int(args[1])
        plan = args[2]

        plan_data = {
            "Starter": (500, 7),
            "Silver": (5000, 15),
            "Gold": (20000, 30)
        }

        if plan not in plan_data:
            return await message.reply_text("❌ Invalid plan. Use Starter, Silver, or Gold.")

        credits, days = plan_data[plan]
        codes = []

        for _ in range(count):
            code = f"BARRY-{gcgenfunc()}-{gcgenfunc()}-{gcgenfunc()}"
            insert_giftcode(code, plan, credits, days)
            codes.append(code)

        msg = f"BARRY [GIFT CODES - {plan.upper()}]\n━━━━━━━━━━━━━\n"
        for code in codes:
            msg += f"[ϟ] Code: <code>{code}</code>\n[ϟ] Plan: {plan} ({days} Days)\n[ϟ] Status: Active ✅\n━━━━━━━━━━━━━\n"
        msg += "Redeem using: <code>/redeem YOUR_CODE</code>"

        await message.reply_text(msg)

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")