from plugins.func.utils import randgen
from plugins.admin.gc.gc_func import gcgenfunc, insert_plan1
from pyrogram import Client, filters
from pyrogram.types import Message

CEO_ID = 6440962840  # Your owner ID

@Client.on_message(filters.command("sub1", prefixes=["/", "."]))
async def cmd_sub1(client: Client, message: Message):
    if message.from_user.id != CEO_ID:
        await message.reply_text("⚠️ Requires Owner Privileges", quote=True)
        return

    try:
        parts = message.text.split()
        amount = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 10
        amount = min(max(amount, 1), 100)  # limit to 1–100

        progress = await message.reply_text(f"⚙️ Generating {amount} Starter Giftcodes...", quote=True)

        linked_ϟ = '<a href="https://t.me/+CUKFuQJYJTUwZmU8">ϟ</a>'  # linked ϟ symbol
        codes = []

        for i in range(1, amount + 1):
            code = f"BARRY-{gcgenfunc()}-{gcgenfunc()}-{gcgenfunc()}"
            insert_plan1(code)
            codes.append(code)
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=progress.id,
                text=f"⏳ Generating: {i}/{amount}"
            )

        # Build message in chunks
        message_parts = []
        current_block = f"BARRY [GIFT CODES - STARTER]\n━━━━━━━━━━━━━\n"

        for code in codes:
            block = (
                f"[{linked_ϟ}] Code: <code>{code}</code>\n"
                f"[{linked_ϟ}] Plan: Starter (7 Days)\n"
                f"[{linked_ϟ}] Status: Active ✅\n"
                "━━━━━━━━━━━━━\n"
            )
            if len(current_block + block) > 3800:
                message_parts.append(current_block)
                current_block = ""
            current_block += block

        if current_block:
            message_parts.append(current_block)

        for part in message_parts:
            await client.send_message(
                chat_id=message.chat.id,
                text=part + "Redeem using: <code>/redeem YOUR_CODE</code>"
            )

        await progress.delete()

    except Exception as e:
        await message.reply_text(f"❌ Error: <code>{e}</code>", quote=True)
