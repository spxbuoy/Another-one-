from pyrogram import Client, filters
import os

@Client.on_message(filters.command("gethits", ["/", "."]))
async def get_charged_file(client, message):
    args = message.text.split()
    if len(args) != 2:
        return await message.reply_text("⚠️ Usage: /gethits KEY", quote=True)

    key = args[1].strip()
    file_path = f"HITS/CHARGED_{key}.txt"

    if os.path.exists(file_path):
        await message.reply_document(file_path, caption=f"✅ Charged CCs for key: {key}", quote=True)
    else:
        await message.reply_text("❌ No charged cards found for this key.", quote=True)