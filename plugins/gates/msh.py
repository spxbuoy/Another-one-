from pyrogram import Client, filters
import re, time, asyncio
from plugins.func.users_sql import *
from plugins.gates.func.mass_shopify_func import shopify_func

@Client.on_message(filters.command("msh"))
async def cmd_msh(Client, message):
    try:
        user_id = str(message.from_user.id)
        user_name = message.from_user.first_name
        chat_id = message.chat.id

        reg = fetchinfo(user_id)
        if not reg:
            return await message.reply_text("You are not registered. Use /register first.", message.id)

        role = reg[2]
        credit = int(reg[5])
        antispam_time = int(reg[7])
        now = int(time.time())

        GROUP = open("plugins/group.txt").read().splitlines()
        chat_type = str(message.chat.type)

        if chat_type == "ChatType.PRIVATE" and role == "FREE":
            return await message.reply_text("Only premium users can use in PM.", message.id)
        if chat_type in ["ChatType.GROUP", "ChatType.SUPERGROUP"] and str(chat_id) not in GROUP:
            return await message.reply_text("Unauthorized chat.", message.id)
        if credit < 1:
            return await message.reply_text("Insufficient credit.", message.id)

        cooldown = 25 if role == "FREE" else 10
        if now - antispam_time < cooldown:
            wait = cooldown - (now - antispam_time)
            return await message.reply_text(f"⏳ AntiSpam: wait {wait}s", message.id)

        # Extract cards
        if message.reply_to_message:
            raw = message.reply_to_message.text.strip().split("\n")
        else:
            raw = message.text.replace("/msh", "").strip().split("\n")

        cards = []
        for x in raw:
            nums = re.findall(r"\d+", x)
            if len(nums) >= 4:
                cards.append([nums[0], nums[1], nums[2], nums[3]])

        if not cards:
            return await message.reply_text("No valid cards provided.", message.id)

        if role == "FREE" and len(cards) > 5:
            return await message.reply_text("Free users can only check 5 cards.")
        if role == "PREMIUM" and len(cards) > 15:
            return await message.reply_text("Premium users can only check 15 cards.")

        start_time = time.time()
        stmsg = await message.reply_text("Please wait...⌛️", reply_to_message_id=message.id)

        text = "BARRY | M Shopify 0.99$\n"

        # Async shopify checks
        tasks = [shopify_func(None, c[0], c[3], c[1], c[2]) for c in cards]
        results = await asyncio.gather(*tasks)

        for i, res in enumerate(results):
            cc = f"{cards[i][0]}|{cards[i][1]}|{cards[i][2]}|{cards[i][3]}"
            status = res.get("status", "❓")
            msg = res.get("response", "No response")

            if "3ds" in msg.lower() or "authentication" in msg.lower():
                status = "3D ❌"
                msg = "3DS Auth Required"

            if "request failed" in msg.lower() or "error" in msg.lower():
                status = "Error"
                msg = msg or "No response from gateway"

            if "approved" in status.lower():
                status = "Approved ✅"

            text += f"Card: <code>{cc}</code>\nStatus: {status}\nResult: {msg}\n━━━━━━━━━━━━━\n"

        t_sec = round(time.time() - start_time, 2)
        mention = f'{user_name}'
        dev = '<a href="tg://user?id=6440962840">𝑩𝑨𝑹𝑹𝒀</a>'
        text += f"[ϟ] T/t: 0.m {int(t_sec)}sec P/x: [Live ⛅]\n"
        text += f"[ϟ] Checked By: {mention} [ {role} ]\n[⌥] Dev: {dev}"

        await Client.edit_message_text(chat_id, stmsg.id, text)
        updatedata(user_id, "credits", credit - len(cards))
        updatedata(user_id, "antispam_time", now)

    except Exception as e:
        await message.reply_text(f"❌ Mass Check Failed: {str(e)}")