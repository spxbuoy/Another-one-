from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
import requests, re, time
from plugins.func.users_sql import fetchinfo, updatedata, plan_expirychk
from datetime import date

session = requests.Session()

@Client.on_message(filters.command("vbv", prefixes=["/", "."]))
async def cmd_vbv(client, message):
    try:
        user_id = str(message.from_user.id)
        chat_id = message.chat.id
        chat_type = message.chat.type
        username = message.from_user.username or "None"

        regdata = fetchinfo(user_id)
        if not regdata:
            return await message.reply_text("❌ You are not registered. Use /register first.")

        role = (regdata[2] or "FREE").strip().upper()
        credit = int(regdata[5] or 0)
        wait_time = int(regdata[6] or (15 if role == "FREE" else 5))
        antispam_time = int(regdata[7] or 0)
        now = int(time.time())

        with open("plugins/group.txt") as f:
            GROUP = f.read().splitlines()

        if chat_type == ChatType.PRIVATE and role == "FREE":
            return await message.reply_text(
                "⚠️ <b>Premium Users Required</b>\nOnly Premium users can use this in PM.\nJoin group for free use:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Join Group", url="https://t.me/+Rl9oTRlGfbIwZDhk")]
                ]),
                disable_web_page_preview=True
            )

        if chat_type in [ChatType.GROUP, ChatType.SUPERGROUP] and str(chat_id) not in GROUP:
            return await message.reply_text("❌ Unauthorized group. Contact admin.")

        if credit < 1:
            return await message.reply_text("❌ Insufficient credit.")
        if now - antispam_time < wait_time:
            return await message.reply_text(f"⏳ Wait {wait_time - (now - antispam_time)}s (AntiSpam)")

        cc_raw = message.reply_to_message.text if message.reply_to_message else (
            message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
        )
        if not cc_raw:
            return await message.reply_text("❌ Usage: /vbv <cc|mm|yy|cvv>")

        match = re.search(r'(\d{12,16})[|:\s,\-]?(\d{1,2})[|:\s,\-]?(\d{2,4})[|:\s,\-]?(\d{3,4})', cc_raw)
        if not match:
            return await message.reply_text("❌ Invalid format. Use: CC|MM|YY|CVV")

        ccnum, mes, ano, cvv = match.groups()
        fullcc = f"{ccnum}|{mes}|{ano}|{cvv}"

        check_msg = await message.reply_text(f"""
<code>┏━━━━━━━⍟</code>
<b>┃  VBV Check</b>
<code>┗━━━━━━━━━━━⊛</code>
<b>⊙ CC:</b> <code>{fullcc}</code>
<b>⊙ Status:</b> Checking...
<b>⊙ Response:</b> Waiting...
""")

        tic = time.perf_counter()

        try:
            res = session.get(f"https://api.voidapi.xyz/v2/vbv?card={fullcc}", timeout=15)
            data = res.json()
            vbv_status = data.get("vbv_status", "").lower()
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

        # BIN Lookup via VoidAPI
        try:
            binres = session.get(f"https://api.voidex.dev/api/bin?bin={ccnum[:6]}", timeout=10).json()
            brand = str(binres.get("brand") or binres.get("scheme") or "N/A").upper()
            type_ = str(binres.get("type", "N/A")).upper()
            level = str(binres.get("level", "N/A")).upper()
            bank = str(binres.get("bank", "N/A")).upper()
            country = str(binres.get("country_name", "N/A")).upper()
            flag = binres.get("country_flag", "🏳️")
        except:
            brand = type_ = level = bank = country = "N/A"
            flag = "🏳️"

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
