from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re, time, asyncio
from datetime import date
from plugins.func.users_sql import fetchinfo, insert_reg_data, updatedata
from plugins.gates.func.mass_auth_func import async_auth_func

@Client.on_message(filters.command("mass", prefixes=["/", "."]))
async def cmd_mass(Client, message):
    try:
        user_id = str(message.from_user.id)
        username = message.from_user.username or "None"
        user_name = message.from_user.first_name
        chat_id = message.chat.id
        msg_id = message.id
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
                "Premium Only in DM.\nJoin group to use for free.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Join Group", url="https://t.me/BarryxChat")]]
                )
            )

        if chat_type in ["ChatType.GROUP", "ChatType.SUPERGROUP"] and str(chat_id) not in GROUP:
            return await message.reply_text("Unauthorized group.")

        if credit < 1:
            return await message.reply_text("❌ Insufficient credit.")

        cooldown = 25 if role == "FREE" else 10
        if now - antispam_time < cooldown:
            wait = cooldown - (now - antispam_time)
            return await message.reply_text(f"⏳ AntiSpam: wait {wait}s")

        cc_input = message.reply_to_message.text if message.reply_to_message else message.text.replace("/mass", "").replace(".mass", "")
        found = re.findall(r'\d{12,16}\D\d{1,2}\D\d{2,4}\D\d{3,4}', cc_input)
        cards = []
        for line in found:
            clean = re.sub(r"[^\d]", "|", line)
            parts = clean.split("|")
            if len(parts) >= 4:
                cards.append(parts[:4])

        if not cards:
            return await message.reply_text("❌ No valid cards found.")
        if role == "FREE" and len(cards) > 5:
            return await message.reply_text("❌ Free users can only check 5 cards.")
        if role == "PREMIUM" and len(cards) > 15:
            return await message.reply_text("❌ Premium users can only check 15 cards.")

        start_time = time.time()
        reply_msg = await message.reply_text("Checking cards...⌛", reply_to_message_id=msg_id)

        proxies = [
            "proxy.rampageproxies.com:5000:package-1111111-country-us:5671nuWwEPrHCw2t",
            "proxy.proxiware.com:1337:user-default-network-res-country-us:OedbOv0g3JOQ"
        ]

        tasks = []
        for i, c in enumerate(cards):
            fullcc = f"{c[0]}|{c[1]}|{c[2]}|{c[3]}"
            proxy = proxies[i % len(proxies)]
            tasks.append(async_auth_func(fullcc, proxy))

        results = await asyncio.gather(*tasks)

        text = "<b> BARRY | MASS STRIPE AUTH</b>\n━━━━━━━━━━━━━\n"
        approved = declined = error = 0

        for i, res in enumerate(results):
            cc = f"{cards[i][0]}|{cards[i][1]}|{cards[i][2]}|{cards[i][3]}"
            status = res.get("status", "Error ❗")
            msg = res.get("response", "No response")

            if "approved" in status.lower():
                approved += 1
            elif "declined" in status.lower():
                declined += 1
            elif "error" in status.lower():
                error += 1

            text += f"<b>⊙ Card:</b> <code>{cc}</code>\n"
            text += f"<b>⊙ Status:</b> {status}\n"
            text += f"<b>⊙ Result:</b> {msg}\n━━━━━━━━━━━━━\n"

        total_time = round(time.time() - start_time, 2)
        dev = '<a href="tg://user?id=6440962840">𝑩𝑨𝑹𝑹𝒀</a>'

        text += f"<b>[✓] Approved:</b> {approved}  |  <b>[✘] Declined:</b> {declined}  |  <b>[!] Error:</b> {error}\n"
        text += f"<b>[ϟ] Time:</b> {total_time}s\n<b>[ϟ] Checked By:</b> {user_name} [ {role} ]\n<b>[⌥] Dev:</b> {dev}"

        await Client.edit_message_text(chat_id=chat_id, message_id=reply_msg.id, text=text, disable_web_page_preview=True)
        updatedata(user_id, "credits", credit - len(cards))
        updatedata(user_id, "antispam_time", now)

    except Exception as e:
        await message.reply_text(f"❌ Mass Check Failed: {str(e)}")
