from pyrogram import Client, filters
import re
import io

def clean_html_tags(text):
    return re.sub(r'<.*?>', '', text)

def is_valid_card(line):
    regex = r'[0-9a-zA-Z]{15,16}[|:/\-_][0-9a-zA-Z]{1,2}[|:/\-_][A-Za-z0-9]{2,4}[|:/\-_][0-9a-z]{3,4}'
    return re.search(regex, line)

def extract_cards(text):
    regex = r'[0-9a-zA-Z]{15,16}[|:/\-_][0-9a-zA-Z]{1,2}[|:/\-_][A-Za-z0-9]{2,4}[|:/\-_][0-9a-z]{3,4}'
    matches = re.findall(regex, text)
    cleaned = [re.sub(r'[/:]', '|', m) for m in matches if m[0] in ['3', '4', '5', '6']]
    return list(set(cleaned))

@Client.on_message(filters.command("sort"))
async def sort_ccs_from_text(client, message):
    if not message.reply_to_message or not message.reply_to_message.text:
        return await message.reply("❌ Reply to a message containing CCs in text format.")

    raw = clean_html_tags(message.reply_to_message.text)
    cards = extract_cards(raw)

    if not cards:
        return await message.reply("❌ No valid cards found in the text.")

    file = io.BytesIO("\n".join(cards).encode())
    file.name = "sorted_cards.txt"

    await message.reply_document(file, caption=f"✅ Sorted {len(cards)} cards from text.")