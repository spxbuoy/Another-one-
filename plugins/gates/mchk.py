from pyrogram import Client, filters
import re, time, concurrent.futures
from plugins.func.users_sql import *
from plugins.gates.func.mass_auth_func import auth_func
from datetime import date
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("mchk"))
async def cmd_mchk(Client, message):
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
                    [[InlineKeyboardButton("Join Group", url="https://t.me/BarryxChat")]]
                ),
                disable_web_page_preview=True
            )

        if chat_type in ["ChatType.GROUP", "ChatType.SUPERGROUP"] and str(chat_id) not in GROUP:
            return await message.reply_text("Unauthorized chat. Contact admin.", message.id)

        if credit < 1:
            return await message.reply_text("❌ Insufficient credit.", message.id)

        cooldown = 25 if role == "FREE" else 10
        if now - antispam_time < cooldown:
            wait = cooldown - (now - antispam_time)
            return await message.reply_text(f"⏳ AntiSpam: wait {wait}s", message.id)

        raw = (message.reply_to_message.text if message.reply_to_message else message.text.replace("/mchk", "")).strip().split("\n")
        cards = []
        for x in raw:
            nums = re.findall(r"\d+", x)
            if len(nums) >= 4:
                cards.append([nums[0], nums[1], nums[2], nums[3]])

        if not cards:
            return await message.reply_text("❌ No valid cards found.", message.id)
        if role == "FREE" and len(cards) > 5:
            return await message.reply_text("Free users can only check 5 cards.")
        if role == "PREMIUM" and len(cards) > 15:
            return await message.reply_text("Premium users can only check 15 cards.")

        start_time = time.time()
        stmsg = await message.reply_text("Please wait...⌛", reply_to_message_id=message.id)

        text = "<b>𝑩𝑨𝑹𝑹𝒀 | M-Stripe 1$ Charge</b>\n━━━━━━━━━━━━━\n"

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(auth_func, None, c[0], c[3], c[1], c[2]) for c in cards]
            for i, f in enumerate(futures):
                res = f.result()
                cc = f"{cards[i][0]}|{cards[i][1]}|{cards[i][2]}|{cards[i][3]}"
                status = res.get("status", "❓")
                msg = res.get("response", "No response")
                text += f"<b>⊙ Card:</b> <code>{cc}</code>\n<b>⊙ Status:</b> {status}\n<b>⊙ Result:</b> {msg}\n━━━━━━━━━━━━━\n"

        elapsed = round(time.time() - start_time, 2)
        dev = '<a href="tg://user?id=6440962840">𝑩𝑨𝑹𝑹𝒀</a>'
        text += f"<b>ϟ T/t:</b> 0.m {elapsed}s | P/x: [Live ⛅]\n"
        text += f"<b>ϟ Checked By:</b> {user_name} [ {role} ]\n<b>⌥ Dev:</b> {dev}"

        await Client.edit_message_text(chat_id, stmsg.id, text)
        updatedata(user_id, "credits", credit - len(cards))
        updatedata(user_id, "antispam_time", now)

    except Exception as e:
        await message.reply_text(f"❌ Mass Check Failed: {str(e)}")