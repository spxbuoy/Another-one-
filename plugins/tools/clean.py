from pyrogram import Client, filters
import re, os, tempfile
from datetime import datetime

def clean_html_tags(text):
    return re.sub(r'<.*?>', '', text)

def extract_card(line):
    pattern = r'[0-9]{15,16}[|:/\-_][0-9]{1,2}[|:/\-_][0-9]{2,4}[|:/\-_][0-9]{3,4}'
    return re.search(pattern, line)

def format_card(raw):
    return re.sub(r'[/:]', '|', raw.strip())

def is_expired(mm, yy):
    try:
        now = datetime.now()
        year = int("20" + yy) if len(yy) == 2 else int(yy)
        month = int(mm)
        return (year < now.year) or (year == now.year and month < now.month)
    except:
        return False

@Client.on_message(filters.command("clean"))
async def clean_txt(client, message):
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply("❌ Reply to a `.txt` file.")

    doc = message.reply_to_message.document
    if not doc.file_name.endswith(".txt"):
        return await message.reply("❌ Only `.txt` files are supported.")

    # Download file
    try:
        file_path = await client.download_media(doc)
    except Exception as e:
        return await message.reply(f"❌ Download failed:\n{e}")

    seen = set()
    total = 0
    expired = 0
    today = datetime.now().strftime("%Y-%m-%d")

    # Temp file (initially with dummy name)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8")

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
            for line in infile:
                line = clean_html_tags(line)
                match = extract_card(line)
                if not match:
                    continue

                card = format_card(match.group())
                if card in seen:
                    continue
                seen.add(card)

                parts = card.split('|')
                if len(parts) >= 3 and is_expired(parts[1], parts[2]):
                    expired += 1

                temp_file.write(card + "\n")
                total += 1

        temp_file.close()

        if total == 0:
            os.remove(temp_file.name)
            return await message.reply("❌ No valid cards found after cleaning.")

        # Rename to final name with total count
        final_name = f"x{total}_ccclean.txt"
        os.rename(temp_file.name, final_name)

        caption = (
            f"CC Clean success⚡\n"
            f"Date: {today}\n"
            f"Total: {total}\n"
            f"Duplicates: 0\n"
            f"Expired Cards: {expired}"
        )

        await message.reply_document(document=final_name, caption=caption)
        os.remove(final_name)

    finally:
        os.remove(file_path)