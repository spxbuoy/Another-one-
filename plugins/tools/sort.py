import re
import io
import os
from pyrogram import Client, filters

def smart_extract(text):
    lines = text.splitlines()
    cards = []
    temp = {}

    for line in lines:
        
        clean = line.strip()

        
        full_match = re.findall(r'(\d{13,16})\D+(\d{1,2})\D+(\d{2,4})\D+(\d{3,4})', clean)
        if full_match:
            for cc, mm, yy, cvv in full_match:
                mm = mm.zfill(2)
                yy = yy[-2:]
                cards.append(f"{cc}|{mm}|{yy}|{cvv}")
            continue

        
        if 'card' in clean.lower() or re.fullmatch(r'\d{13,16}', clean):
            digits = re.findall(r'\d{13,16}', clean)
            if digits:
                temp['cc'] = digits[0]
        elif 'exp' in clean.lower():
            exp = re.findall(r'(\d{1,2})[\/\-](\d{2,4})', clean)
            if exp:
                temp['mm'], temp['yy'] = exp[0]
        elif 'cvv' in clean.lower() or 'cvc' in clean.lower():
            cvv = re.findall(r'\d{3,4}', clean)
            if cvv:
                temp['cvv'] = cvv[0]

        
        if all(k in temp for k in ['cc', 'mm', 'yy', 'cvv']):
            mm = temp['mm'].zfill(2)
            yy = temp['yy'][-2:]
            cards.append(f"{temp['cc']}|{mm}|{yy}|{temp['cvv']}")
            temp = {}

    return list(set(cards)) 

@Client.on_message(filters.command("sort", [".", "/"]))
async def filter_any_format(client, message):
    try:
        input_text = None

        if message.reply_to_message:
            if message.reply_to_message.document:
                file = await message.reply_to_message.download()
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    input_text = f.read()
                os.remove(file)
            else:
                input_text = message.reply_to_message.text
        else:
            input_text = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""

        if not input_text:
            return await message.reply("No input found to extract. ❌")

        cards = smart_extract(input_text)

        if cards:
            result = "\n".join(cards)
            if len(cards) >= 32:
                file = io.BytesIO(result.encode())
                file.name = "sort.txt"
                await message.reply_document(file, caption=f"Extracted {len(cards)} cards. ✅")
            else:
                await message.reply_text(f"<code>{result}</code>", quote=True)
        else:
            await message.reply("No valid cards found in input. ⚠️", quote=True)

    except Exception as e:
        await message.reply(f"Error: {str(e)} ❌")
