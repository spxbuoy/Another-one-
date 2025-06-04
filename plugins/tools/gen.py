import re, time, requests, random
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from plugins.func.users_sql import fetchinfo

async def checkLuhn(cardNo):
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False
    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord("0")
        if isSecond:
            d = d * 2
        nSum += d // 10
        nSum += d % 10
        isSecond = not isSecond
    return nSum % 10 == 0

async def cc_genarator(cc, mes, ano, cvv):
    cc, mes, ano, cvv = str(cc), str(mes), str(ano), str(cvv)
    if mes != "None" and len(mes) == 1:
        mes = "0" + mes
    if ano != "None" and len(ano) == 2:
        ano = "20" + ano
    numbers = list("0123456789")
    random.shuffle(numbers)
    result = "".join(numbers)
    result = cc + result
    if cc.startswith(("34", "37")):
        cc = result[:15]
    else:
        cc = result[:16]
    for i in range(len(cc)):
        if cc[i] == 'x':
            cc = cc[:i] + str(random.randint(0, 9)) + cc[i+1:]
    if mes == "None" or 'X' in mes or 'x' in mes or 'rnd' in mes:
        mes = str(random.randint(1, 12)).zfill(2)
    if ano == "None" or 'X' in ano or 'x' in ano or 'rnd' in ano:
        ano = str(random.randint(2024, 2035))
    if cvv == "None" or 'x' in cvv or 'X' in cvv or 'rnd' in cvv:
        cvv = str(random.randint(1000, 9999)) if cc.startswith(("34", "37")) else str(random.randint(100, 999))
    return f"{cc}|{mes}|{ano}|{cvv}"

async def luhn_card_genarator(cc, mes, ano, cvv, amount):
    all_cards = []
    for _ in range(amount):
        while True:
            result = await cc_genarator(cc, mes, ano, cvv)
            ccx, mesx, anox, cvvx = result.split("|")
            if await checkLuhn(ccx):
                all_cards.append(f"{ccx}|{mesx}|{anox}|{cvvx}")
                break
    return all_cards

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
        amount = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else None
    except:
        return await message.reply("<b>[ϟ] Use: /gen 400363 or /gen 400363 10</b>")

    if len(bin_input) < 6 or not bin_input[:6].isdigit():
        return await message.reply("<b>[ϟ] Invalid BIN. Use: /gen 400363</b>")

    bin_code = bin_input[:6]
    gen_amount = amount if amount else 10
    start = time.perf_counter()

    try:
        bin_data = requests.get(f"https://api.voidex.dev/api/bin?bin={bin_code}", timeout=10).json()
        brand = bin_data.get("brand", "Unknown")
        card_type = bin_data.get("type", "Unknown")
        level = bin_data.get("level", "Unknown")
        bank = bin_data.get("bank", "Unknown")
        country = bin_data.get("country_name", "Unknown")
        flag = bin_data.get("country_flag", "🏳")
    except:
        brand = card_type = level = bank = country = "Unknown"
        flag = "🏳"

    cards_list = await luhn_card_genarator(bin_code + "xxxxxxxxxxxx", "rnd", "rnd", "rnd", gen_amount)
    cards_raw = "\n".join(cards_list)

    # Prepare .txt file
    card_file = BytesIO()
    card_file.write(cards_raw.encode("utf-8"))
    card_file.name = f"{bin_code}_cards.txt"
    card_file.seek(0)

    linked_ϟ = '<a href="https://t.me/+CUKFuQJYJTUwZmU8">ϟ</a>'

    if amount:
        # Only send TXT file
        await client.send_document(
            chat_id=message.chat.id,
            document=card_file,
            caption=f"<b>[{linked_ϟ}] Generated {amount} CCs from BIN {bin_code}</b>",
            reply_to_message_id=message.id
        )
    else:
        # Show message with CCs in <code> lines
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
