from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.utils import randgen
from plugins.admin.gc.gc_func import gcgenfunc, insert_giftcode

CEO_ID = 6440962840  # Your Owner ID

@Client.on_message(filters.command("gc", prefixes=["/", "."]))
async def cmd_gc(client: Client, message: Message):
    if message.from_user.id != CEO_ID:
        await message.reply_text("❌ Requires Owner Privileges", quote=True)
        return

    try:
        args = message.text.split()
        count = int(args[1]) if len(args) > 1 else 10
        days = int(args[2]) if len(args) > 2 else 30
        credits = int(args[3]) if len(args) > 3 else 2000

        count = max(1, min(count, 100))
        days = max(1, min(days, 3650))

        status_msg = await message.reply_text("Generating giftcodes...", quote=True)
        codes = []

        for i in range(1, count + 1):
            code = f"BARRY-{gcgenfunc()}-{gcgenfunc()}-{gcgenfunc()}"
            insert_giftcode(code, f"PREMIUM_{days}", credits, days)
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
                f"[ϟ] Value: {credits} Credits\n"
                f"[ϟ] Status: Active ✅\n"
                "━━━━━━━━━━━━━\n"
            )
        final_msg += "Redeem using: <code>/redeem CODE</code>"

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