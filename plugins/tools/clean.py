from pyrogram import Client, filters
import re, os, tempfile, json
from datetime import datetime

def clean_html_tags(text):
    return re.sub(r'<.*?>', '', text)

def extract_card(text):
    
    card_pattern = r'(\d{12,16})[^\d]{1,3}(\d{1,2})[^\d]{1,3}(\d{2,4})[^\d]{1,3}(\d{3,4})'
    return re.findall(card_pattern, text)

def extract_card_from_json(line):
    try:
        d = json.loads(line.replace("'", '"'))
        card = d.get("card_num") or ""
        cvv = d.get("cvv") or ""
        expiry = d.get("expiry_date") or ""
        if len(expiry) == 6:  
            return f"{card}|{expiry[:2]}|{expiry[2:]}|{cvv}"
    except:
        pass
    return None

def is_expired(mm, yy):
    try:
        now = datetime.now()
        year = int("20" + yy) if len(yy) == 2 else int(yy)
        month = int(mm)
        return (year < now.year) or (year == now.year and month < now.month)
    except:
        return False

@Client.on_message(filters.command(["clean", ".clean", "/clean"]))
async def clean_txt(client, message):
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply("❌ Reply to a .txt file to clean cards.")

    doc = message.reply_to_message.document
    if not doc.file_name.endswith(".txt"):
        return await message.reply("❌ Only `.txt` files are supported.")

    try:
        file_path = await client.download_media(doc)
    except Exception as e:
        return await message.reply(f"❌ Download failed:\n{e}")

    seen = set()
    total = 0
    expired = 0
    today = datetime.now().strftime("%Y-%m-%d")

    cleaned_cards = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = clean_html_tags(line.strip())

            
            json_card = extract_card_from_json(line)
            if json_card:
                parts = json_card.split("|")
                if json_card not in seen:
                    seen.add(json_card)
                    if len(parts) >= 3 and is_expired(parts[1], parts[2]):
                        expired += 1
                    cleaned_cards.append(json_card)
                    total += 1
                continue

            
            matches = extract_card(line)
            for ccnum, mes, ano, cvv in matches:
                formatted = f"{ccnum}|{mes}|{ano}|{cvv}"
                if formatted in seen:
                    continue
                seen.add(formatted)
                if is_expired(mes, ano):
                    expired += 1
                cleaned_cards.append(formatted)
                total += 1

    os.remove(file_path)

    if total == 0:
        return await message.reply("❌ No valid cards found after cleaning.")

    
    filename = f"x{total}_ccclean.txt"
    with open(filename, "w") as f:
        f.write("\n".join(cleaned_cards))

    caption = (
        f"<b>CC Cleaned success⚡</b>\n"
        f"Date: {today}\n"
        f"Total: <code>{total}</code>\n"
        f"Expired: <code>{expired}</code>\n"
        f"Duplicates Removed: <code>{len(seen) - total + expired}</code>"
    )

    await message.reply_document(document=filename, caption=caption)
    os.remove(filename)
