from plugins.func.utils import randgen
from plugins.admin.gc.gc_func import gcgenfunc, insert_plan1
from pyrogram import Client, filters
from pyrogram.types import Message

CEO_ID = 6440962840  # Your owner ID

@Client.on_message(filters.command("sub1"))
async def cmd_sub1(client: Client, message: Message):
    if message.from_user.id != CEO_ID:
        await message.reply_text("⚠️ Requires Owner Privileges", quote=True)
        return

    try:
        parts = message.text.split()
        amount = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 10
        amount = min(max(amount, 1), 100)  # limit to 1–100

        progress = await message.reply_text(f"⚙️ Generating {amount} Starter Giftcodes...", quote=True)

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

        final_msg = f"BARRY [GIFT CODES - STARTER]\n━━━━━━━━━━━━━\n"
        for code in codes:
            final_msg += (
                f"[ϟ] Code: <code>{code}</code>\n"
                f"[ϟ] Plan: Starter (7 Days)\n"
                f"[ϟ] Status: Active ✅\n"
                "━━━━━━━━━━━━━\n"
            )
        final_msg += "Redeem using: <code>/redeem YOUR_CODE</code>"

        await client.edit_message_text(
            chat_id=message.chat.id,
            message_id=progress.id,
            text=final_msg
        )

    except Exception as e:
        await message.reply_text(f"❌ Error: <code>{e}</code>", quote=True)