from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.utils import randgen
from plugins.admin.gc.gc_func import gcgenfunc, insert_giftcode

CEO_ID = 6440962840  # Owner ID

@Client.on_message(filters.command("gc"))
async def cmd_gc(client: Client, message: Message):
    if message.from_user.id != CEO_ID:
        await message.reply_text("❌ Requires Owner Privileges", quote=True)
        return

    try:
        args = message.text.split()
        count = 10  # Default giftcodes
        days = 30   # Default validity

        if len(args) > 1:
            try:
                count = int(args[1])
                if count < 1 or count > 100:
                    await message.reply_text("Please enter a valid number (1–100).", quote=True)
                    return
            except ValueError:
                await message.reply_text("Usage: /gc [amount] [days]", quote=True)
                return

        if len(args) > 2:
            try:
                days = int(args[2])
                if days < 1 or days > 3650:
                    await message.reply_text("Please enter valid days (1–3650).", quote=True)
                    return
            except ValueError:
                await message.reply_text("Usage: /gc [amount] [days]", quote=True)
                return

        status_msg = await message.reply_text("Generating giftcodes...", quote=True)
        codes = []

        for i in range(1, count + 1):
            code = f"BARRY-{gcgenfunc()}-{gcgenfunc()}-{gcgenfunc()}"
            insert_giftcode(code, f"PREMIUM_{days}")
            codes.append(code)
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=status_msg.id,
                text=f"Generating: {i}/{count}"
            )

        final_msg = f"BARRY [GIFTCODES - PREMIUM {days} DAYS]\n━━━━━━━━━━━━━\n"
        for code in codes:
            final_msg += (
                f"[ϟ] Code: <code>{code}</code>\n"
                f"[ϟ] Plan: Premium ({days} Days)\n"
                f"[ϟ] Value: 5000 Credits\n"
                f"[ϟ] Status: Active ✅\n"
                "━━━━━━━━━━━━━\n"
            )
        final_msg += "Redeem using: <code>/redeem CODE</code>"

        # Handle Telegram's max message length
        if len(final_msg) > 4000:
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=status_msg.id,
                text="✅ Giftcodes generated. Sending in parts..."
            )
            for chunk in [final_msg[i:i+4000] for i in range(0, len(final_msg), 4000)]:
                await client.send_message(message.chat.id, chunk)
        else:
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=status_msg.id,
                text=final_msg
            )

    except Exception as e:
        await message.reply_text(f"❌ Error: <code>{e}</code>", quote=True)