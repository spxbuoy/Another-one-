from pyrogram import Client, filters
from pyrogram.types import Message

FEEDBACK_CHANNEL = -1002355656869

@Client.on_message(filters.command(["rev", ".rev"]))
async def handle_rev(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply(
            "Please Reply To An Image To Submit Feedback!"
        )

    
    if message.from_user.id != message.reply_to_message.from_user.id:
        return await message.reply(
            "You can only submit feedback for photos you’ve sent yourself. 🚫"
        )

    user = message.from_user
    extra_text = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else ""

    caption = f"Feedback received from @{user.username or 'anonymous'} (ID: {user.id})"
    if extra_text:
        caption += f"\n\n🗒️ Comment:\n{extra_text}"

    try:
        await client.send_photo(
            chat_id=FEEDBACK_CHANNEL,
            photo=message.reply_to_message.photo.file_id,
            caption=caption
        )
        await message.reply("Thank you for your feedback! Our team will review it shortly. 💬")
    except Exception as e:
        await message.reply(f"Oops! Failed to send your feedback.\nError: {e} ⚠️")
