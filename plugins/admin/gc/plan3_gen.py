from plugins.func.utils import randgen
from plugins.admin.gc.gc_func import gcgenfunc, insert_plan3
from pyrogram import Client, filters
from pyrogram.types import Message

CEO_ID = 6440962840  # Owner ID

@Client.on_message(filters.command("sub3"))
async def cmd_sub3(client: Client, message: Message):
    if message.from_user.id != CEO_ID:
        await message.reply_text("⚠️ Requires Owner Privileges", quote=True)
        return

    try:
        parts = message.text.split()
        amount = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1
        amount = min(max(amount, 1), 100)  # Limit between 1 and 100

        loading = await message.reply_text(f"⚙️ Generating {amount} Gold Giftcodes...", quote=True)
        codes = []

        linked_ϟ = '<a href="https://t.me/+CUKFuQJYJTUwZmU8">ϟ</a>'  # Clickable link symbol

        for i in range(1, amount + 1):
            code = f"BARRY-{gcgenfunc()}-{gcgenfunc()}-{gcgenfunc()}"
            insert_plan3(code)
            codes.append(code)
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=loading.id,
                text=f"⏳ Generating: {i}/{amount}"
            )

        final_msg = "BARRY [GIFT CODES - GOLD]\n━━━━━━━━━━━━━\n"
        for code in codes:
            final_msg += (
                f"[{linked_ϟ}] Code: <code>{code}</code>\n"
                f"[{linked_ϟ}] Plan: Gold (30 Days)\n"
                f"[{linked_ϟ}] Status: Active ✅\n"
                "━━━━━━━━━━━━━\n"
            )
        final_msg += "Redeem using: <code>/redeem CODE</code>"

        await client.edit_message_text(
            chat_id=message.chat.id,
            message_id=loading.id,
            text=final_msg
        )

    except Exception as e:
        await message.reply_text(f"❌ Error: <code>{e}</code>", quote=True)
