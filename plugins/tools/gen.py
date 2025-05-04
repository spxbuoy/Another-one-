import re, time, requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.func.utils import cc_gen
from plugins.func.users_sql import fetchinfo

@Client.on_message(filters.command("gen", ["/", "."]))
async def gen(client, message):
    user_id = message.from_user.id
    chat_type = message.chat.type

    if chat_type == "private":
        return await message.reply("<b>[ϟ] You are not allowed to use this command in DM.</b>")

    user_data = fetchinfo(user_id)
    if not user_data:
        return await message.reply("<b>[ϟ] You are not registered. Use /register</b>")

    plan = user_data[2].upper() if len(user_data) > 2 else "FREE"

    try:
        bin_input = message.text.split(" ", 1)[1].strip()
    except IndexError:
        return await message.reply("<b>[ϟ] Use: /gen 400363</b>")

    if len(bin_input) < 6 or not bin_input[:6].isdigit():
        return await message.reply("<b>[ϟ] Invalid BIN. Use: /gen 400363</b>")

    bin_code = bin_input[:6]
    amount = 10
    start = time.perf_counter()

    try:
        bin_data = requests.get(f"https://bins.antipublic.cc/bins/{bin_code}").json()
        brand = bin_data.get("brand", "Unknown")
        card_type = bin_data.get("type", "Unknown")
        level = bin_data.get("level", "Unknown")
        bank = bin_data.get("bank", "Unknown")
        country = bin_data.get("country_name", "Unknown")
        flag = bin_data.get("country_flag", "🏳")
    except:
        brand = card_type = level = bank = country = "Unknown"
        flag = "🏳"

    cards = cc_gen(bin_code)
    duration = time.perf_counter() - start
    mention = f"<a href='tg://user?id={user_id}'>{message.from_user.first_name}</a>"

    result = f"""
[ϟ] 𝗕𝗶𝗻: {bin_code}
[ϟ] 𝗔𝗺𝗼𝘂𝗻𝘁: {amount}
━━━━━━━━━━━━━
{chr(10).join(cards)}
━━━━━━━━━━━━━
[ϟ] 𝗜𝗻𝗳𝗼: {brand} - {card_type} - {level}
[ϟ] 𝗕𝗮𝗻𝗸: {bank}
[ϟ] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country} - [{flag}]
[ϟ] 𝗧𝗶𝗺𝗲: {duration:.2f} sec
[ϟ] 𝗥𝗲𝗾 𝗕𝘆: {mention} [{plan}]
━━━━━━━━━━━━━
"""

    await client.send_message(
        chat_id=message.chat.id,
        text=result,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ 𝗖𝗟𝗢𝗦𝗘", callback_data="close")]
        ])
    )

# Handle the close button (in another file)
@Client.on_callback_query(filters.regex("close"))
async def close_callback(client, callback_query):
    try:
        await callback_query.message.delete()
    except:
        await callback_query.answer("❌ Failed to close.", show_alert=True)