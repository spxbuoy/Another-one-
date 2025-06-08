import re, time, random, httpx
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from plugins.func.users_sql import fetchinfo


# Luhn Check
def checkLuhn(cardNo):
    sum = 0
    alt = False
    for i in range(len(cardNo) - 1, -1, -1):
        n = int(cardNo[i])
        if alt:
            n *= 2
            if n > 9:
                n -= 9
        sum += n
        alt = not alt
    return sum % 10 == 0


# Fill x and correct Luhn
def generate_luhn_card(base: str) -> str:
    incomplete = list(base.replace("x", "0"))
    for i in range(len(base)):
        if base[i] == 'x':
            incomplete[i] = str(random.randint(0, 9))

    for last_digit in range(10):
        incomplete[-1] = str(last_digit)
        if checkLuhn("".join(incomplete)):
            return "".join(incomplete)
    return "".join(incomplete)


# Random MM/YY/CVV logic
def generate_fields(month, year, cvv, base):
    month = (
        str(random.randint(1, 12)).zfill(2)
        if month in ["None", "rnd", "x", "X"] else month.zfill(2)
    )
    year = (
        str(random.randint(2025, 2035))
        if year in ["None", "rnd", "x", "X"] else ("20" + year if len(year) == 2 else year)
    )
    cvv = (
        str(random.randint(1000, 9999)) if base.startswith(("34", "37"))
        else str(random.randint(100, 999))
        if cvv in ["None", "rnd", "x", "X"] else cvv
    )
    return month, year, cvv


# Fast generator with valid Luhn
async def luhn_card_generator_fast(base: str, month, year, cvv, count: int):
    cards = []
    while len(cards) < count:
        gen = generate_luhn_card(base)
        mes, ano, cvv = generate_fields(month, year, cvv, base)
        cards.append(f"{gen}|{mes}|{ano}|{cvv}")
    return cards


@Client.on_message(filters.command("gen", ["/", "."]))
async def gen(client: Client, message: Message):
    user_id = str(message.from_user.id)
    chat_type = message.chat.type

    if chat_type == "private":
        return await message.reply("<b>[ϟ] You are not allowed to use this command in DM.</b>")

    user_data = fetchinfo(user_id)
    if not user_data:
        return await message.reply("<b>[ϟ] You are not registered. Use /register</b>")

    plan = user_data[2].upper() if user_data[2] else "FREE"

    try:
        parts = message.text.split()
        bin_input = parts[1]
        amount = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 10
    except:
        return await message.reply("<b>[ϟ] Use: /gen 400363 or /gen 400363 10</b>")

    if len(bin_input) < 6 or not bin_input[:6].isdigit():
        return await message.reply("<b>[ϟ] Invalid BIN. Use: /gen 400363</b>")

    bin_code = bin_input[:6]
    gen_amount = amount if amount else 10
    start = time.perf_counter()

    # Async BIN info
    try:
        async with httpx.AsyncClient(timeout=10.0) as clientx:
            r = await clientx.get(f"https://api.voidex.dev/api/bin?bin={bin_code}")
            bin_data = r.json()
            brand = bin_data.get("brand", "Unknown")
            card_type = bin_data.get("type", "Unknown")
            level = bin_data.get("level", "Unknown")
            bank = bin_data.get("bank", "Unknown")
            country = bin_data.get("country_name", "Unknown")
            flag = bin_data.get("country_flag", "🏳")
    except:
        brand = card_type = level = bank = country = "Unknown"
        flag = "🏳"

    # Fast Gen
    cards_list = await luhn_card_generator_fast(bin_code + "xxxxxxxxxxxx", "rnd", "rnd", "rnd", gen_amount)
    cards_raw = "\n".join(cards_list)

    # .txt output
    card_file = BytesIO()
    card_file.write(cards_raw.encode("utf-8"))
    card_file.name = f"{bin_code}_cards.txt"
    card_file.seek(0)

    linked_ϟ = '<a href="https://t.me/+CUKFuQJYJTUwZmU8">ϟ</a>'

    if amount >= 15:
        await client.send_document(
            chat_id=message.chat.id,
            document=card_file,
            caption=f"<b>[{linked_ϟ}] Generated {amount} CCs from BIN {bin_code}</b>",
            reply_to_message_id=message.id
        )
    else:
        cards_formatted = "\n".join([f"<code>{card}</code>" for card in cards_list])
        duration = time.perf_counter() - start
        mention = f"<a href='tg://user?id={user_id}'>{message.from_user.first_name}</a>"

        result = f"""
[{linked_ϟ}] 𝗕𝗶𝗻: {bin_code}
[{linked_ϟ}] 𝗔𝗺𝗼𝘂𝗻𝘁: {gen_amount}
━━━━━━━━━━━━━
{cards_formatted}
━━━━━━━━━━━━━
[{linked_ϟ}] 𝗜𝗻𝗳𝗼: {brand} - {card_type} - {level}
[{linked_ϟ}] 𝗕𝗮𝗻𝗸: {bank}
[{linked_ϟ}] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country} - [{flag}]
[{linked_ϟ}] 𝗧𝗶𝗺𝗲: {duration:.2f} sec
[{linked_ϟ}] 𝗥𝗲𝗾 𝗕𝘆: {mention} [{plan}]
━━━━━━━━━━━━━
"""
        await message.reply_text(
            result,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ 𝗖𝗟𝗢𝗦𝗘", callback_data="close")]
            ])
        )


@Client.on_callback_query(filters.regex("close"))
async def close_callback(client: Client, callback_query: CallbackQuery):
    try:
        await callback_query.message.delete()
    except:
        await callback_query.answer("❌ Failed to close.", show_alert=True)
