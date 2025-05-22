from pyrogram import Client, filters
import re
import io

# Optional: remove unwanted HTML tags
def clean_html_tags(text):
    return re.sub(r'<.*?>', '', text)

# Extract and normalize any format to cc|mm|yy|cvv
def extract_cards(text):
    pattern = r'(?:(\d{12,19})\D{0,3}(\d{1,2})\D{0,3}(\d{2,4})\D{0,3}(\d{3,4}))'
    matches = re.findall(pattern, text)

    cleaned = []
    for cc, mm, yy, cvv in matches:
        if not cc or not mm or not yy or not cvv:
            continue
        if not cc.startswith(('3', '4', '5', '6')):
            continue
        if len(cvv) not in [3, 4]:
            continue

        mm = mm.zfill(2)
        yy = yy[-2:]  # Keep last 2 digits (e.g., 2029 → 29)
        cleaned.append(f"{cc}|{mm}|{yy}|{cvv}")

    return list(set(cleaned))  # Remove duplicates

@Client.on_message(filters.command("sort", prefixes=["/", "."]))
async def sort_ccs_from_text(client, message):
    if not message.reply_to_message or not (message.reply_to_message.text or message.reply_to_message.caption):
        return await message.reply("❌ Reply to a message containing CCs in any format.")

    raw = clean_html_tags(message.reply_to_message.text or message.reply_to_message.caption)
    cards = extract_cards(raw)

    if not cards:
        return await message.reply("❌ No valid cards found in the text.")

    file = io.BytesIO("\n".join(cards).encode())
    file.name = "sorted_cards.txt"
    await message.reply_document(file, caption=f"✅ Sorted {len(cards)} cards from text.")
