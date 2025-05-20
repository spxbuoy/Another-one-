from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests, re, time
from plugins.func.users_sql import *
from datetime import date

session = requests.Session()

def get_bin_data(ccnum):
    try:
        # First try binlist.net
        res = session.get(f"https://lookup.binlist.net/{ccnum[:6]}", timeout=10)
        if res.status_code == 200:
            j = res.json()
            return {
                "brand": j.get("scheme", "N/A").upper(),
                "type": j.get("type", "N/A").upper(),
                "level": j.get("brand", "STANDARD").upper(),
                "bank": j.get("bank", {}).get("name", "N/A").upper(),
                "country": j.get("country", {}).get("name", "N/A").upper(),
                "flag": j.get("country", {}).get("emoji", "")
            }
    except:
        pass

    try:
        # Fallback to antipublic.cc
        res = session.get(f"https://bins.antipublic.cc/bins/{ccnum[:6]}", timeout=10)
        if res.status_code == 200:
            j = res.json()
            return {
                "brand": j.get("vendor", "UNKNOWN").upper(),
                "type": j.get("type", "UNKNOWN").upper(),
                "level": j.get("level", "STANDARD").upper(),
                "bank": j.get("bank", "UNKNOWN BANK").upper(),
                "country": j.get("country_name", "UNKNOWN").upper(),
                "flag": j.get("country_flag", "")
            }
    except:
        pass

    return {
        "brand": "UNKNOWN",
        "type": "UNKNOWN",
        "level": "STANDARD",
        "bank": "UNKNOWN BANK",
        "country": "UNKNOWN",
        "flag": ""
    }

@Client.on_message(filters.command("vbv"))
async def cmd_vbv(client, message):
    try:
        user_id = str(message.from_user.id)
        username = message.from_user.username or "None"
        chat_id = message.chat.id
        chat_type = str(message.chat.type)

        regdata = fetchinfo(user_id)
        if not regdata:
            insert_reg_data(user_id, username, 200, str(date.today()))
            regdata = fetchinfo(user_id)

        if not regdata or len(regdata) < 8:
            return await message.reply_text("❌ Registration failed. Contact admin.")

        status = str(regdata[2] or "FREE")
        credit = int(regdata[5] or 0)
        wait_time = int(regdata[6]) if regdata[6] else (15 if status == "FREE" else 5)
        antispam_time = int(regdata[7]) if regdata[7] else 0
        now = int(time.time())

        GROUP = open("plugins/group.txt").read().splitlines()
        if chat_type == "ChatType.PRIVATE" and status == "FREE":
            return await message.reply_text(
                "Premium Users Required ⚠️\nOnly Premium Users can use this in PM.\nJoin group for free use:",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Group", url="https://t.me/BarryxChat")]]),
                disable_web_page_preview=True
            )

        if chat_type in ["ChatType.GROUP", "ChatType.SUPERGROUP"] and str(chat_id) not in GROUP:
            return await message.reply_text("❌ Unauthorized group. Contact admin.")

        if credit < 1:
            return await message.reply_text("❌ Insufficient credit.")

        if now - antispam_time < wait_time:
            return await message.reply_text(f"⏳ AntiSpam: wait {wait_time - (now - antispam_time)}s")

        cc = message.reply_to_message.text if message.reply_to_message else message.text[len('/vbv '):].strip()
        match = re.search(r'(\d{12,16})[|:\s,-](\d{1,2})[|:\s,-](\d{2,4})[|:\s,-](\d{3,4})', cc)
        if not match:
            return await message.reply_text("❌ Invalid format. Use cc|mm|yy|cvv")

        ccnum, mes, ano, cvv = match.groups()
        fullcc = f"{ccnum}|{mes}|{ano}|{cvv}"

        check_msg = await message.reply_text(f"""
┏━━━━━━━⍟
┃  VBV Check
┗━━━━━━━━━━━⊛
⊙ CC: {fullcc}
⊙ Status: Checking...
⊙ Response: Waiting for Response...
""")

        tic = time.perf_counter()
        url = f"https://api.voidapi.xyz/v2/vbv?card={fullcc}"

        try:
            res = session.get(url, timeout=15)
            j = res.json()
            vbv_status = j.get("vbv_status", "").lower()
            card_message = vbv_status or "No response"
        except:
            vbv_status = "error"
            card_message = "VBV API Failed"

        toc = time.perf_counter()

        non_vbv_keywords = [
            "authenticate_successful", 
            "attempt_acknowledged", "authenticate_attempt_successful", "exempted",
            "out_of_scope", "challenge_required_but_attempt_not_performed",
            "challenge_required_but_issuer_not_participating",
            "authentication_not_required", "authentication_unavailable"
        ]

        if any(k in vbv_status for k in non_vbv_keywords):
            status = "NON VBV"
            emoji = "✅"
        else:
            status = "VBV"
            emoji = "❌"

        # Fetch BIN info using combined logic
        bin_data = get_bin_data(ccnum)
        brand = bin_data["brand"]
        type_ = bin_data["type"]
        level = bin_data["level"]
        bank = bin_data["bank"]
        country = bin_data["country"]
        flag = bin_data["flag"]

        final_msg = f"""
<code>┏━━━━━━━⍟</code>
<b>┃  VBV Check</b>
<code>┗━━━━━━━━━━━⊛</code>
<b>⊙ CC:</b> <code>{fullcc}</code>
<b>⊙ Status:</b> {status} {emoji}
<b>⊙ Response:</b> {card_message}
<b>⊙ Bank:</b> {bank}
<b>⊚ Bin type:</b> {brand} - {type_} - {level}
<b>⊙ Country:</b> {country} {flag}
<b>⊙ Time:</b> {toc - tic:.2f}s
<b>❛ ━━━━・⌁ 𝑩𝑨𝑹𝑹𝒀 ⌁・━━━━ ❜</b>
"""

        await client.edit_message_text(chat_id, check_msg.id, final_msg)
        updatedata(user_id, "credits", credit - 1)
        updatedata(user_id, "antispam_time", now)
        plan_expirychk(user_id)

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
