from pyrogram import Client, filters
import requests
from plugins.func.users_sql import fetchinfo, plan_expirychk

@@Client.on_message(filters.command("bin", prefixes=["/", "."]))
async def cmd_bin(client, message):
    user_id = str(message.from_user.id)
    user_info = fetchinfo(user_id)

    if not user_info:
        return await message.reply_text("❌ You're not registered. Use /register first.")

    # Make it synchronous
    plan_expirychk(user_id)

    if message.reply_to_message:
        bin_input = message.reply_to_message.text.strip()
    else:
        try:
            bin_input = message.text.split(maxsplit=1)[1].strip()
        except IndexError:
            return await message.reply_text("⚠️ Usage: /bin 400005")

    if len(bin_input) < 6 or not bin_input[:6].isdigit():
        return await message.reply_text("❌ Please enter a valid 6-digit BIN.")

    bin_number = bin_input[:6]
    try:
        res = requests.get(f"https://lookup.binlist.net/{bin_number}")
        if res.status_code != 200:
            return await message.reply_text("❌ BIN not found or API failed.")
        data = res.json()
    except Exception as e:
        return await message.reply_text(f"❌ Error: {e}")

    brand = str(data.get("scheme", "N/A")).upper()
    type_ = str(data.get("type", "N/A")).upper()
    level = str(data.get("brand", "N/A")).upper()
    bank = str(data.get("bank", {}).get("name", "N/A")).upper()
    country = str(data.get("country", {}).get("name", "N/A")).upper()
    flag = str(data.get("country", {}).get("emoji", ""))
    currency = str(data.get("country", {}).get("currency", "N/A")).upper()
    username = message.from_user.first_name or "User"
    role = user_info[2] or "None"

    reply = f"""
𝗩𝗮𝗹𝗶𝗱 𝗕𝗜𝗡 ✅

𝗕𝗜𝗡:  {bin_number}
𝗕𝗿𝗮𝗻𝗱: {brand}
𝗟𝗲𝘃𝗲𝗹: {level}
𝗧𝘆𝗽𝗲: {type_}
𝗕𝗮𝗻𝗸: {bank}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country} - {flag} - {currency}

𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆  ⏤‌‌{username} [ {role} ]
𝗕𝗼𝘁 𝗕𝘆 𝗕𝗮𝗿𝗿𝘆
"""

    await message.reply_text(reply)
