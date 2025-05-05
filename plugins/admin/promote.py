from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import fetchinfo, updatedata

CEO_ID = 6440962840  # Owner's user ID

@Client.on_message(filters.command("pm"))
async def cmd_pm(client: Client, message: Message):
    try:
        if message.from_user.id != CEO_ID:
            await message.reply_text("⛔ <b>Owner privileges required.</b>", quote=True, )
            return

        # Identify target user
        if message.reply_to_message:
            target_id = message.reply_to_message.from_user.id
        else:
            try:
                target_id = int(message.text.split(maxsplit=1)[1])
            except IndexError:
                await message.reply_text("⚠️ <b>Usage:</b> <code>/pm user_id</code> or reply to a user", quote=True, )
                return

        # Get user info
        user_data = fetchinfo(target_id)
        if not user_data:
            await message.reply_text("❌ <b>User not found in database.</b>", quote=True, )
            return

        status = str(user_data[2])
        if status == "PREMIUM":
            await message.reply_text(
                f"⚠️ <a href='tg://user?id={target_id}'>{target_id}</a> is already a <b>PREMIUM</b> member.",
                quote=True, 
            )
        else:
            updatedata(target_id, "status", "PREMIUM")
            await message.reply_text(
                f"✅ <a href='tg://user?id={target_id}'>{target_id}</a> has been <b>PROMOTED</b> to <b>PREMIUM</b>.",
                quote=True, 
            )
            await client.send_message(
                target_id,
                "🎉 <b>Congratulations!</b>\n\n"
                "Your account has been <b>UPGRADED to PREMIUM</b> ✅\n"
                "Enjoy access to premium features!",
                
            )

    except Exception as e:
        await message.reply_text(f"❌ <b>Error:</b> <code>{e}</code>", quote=True, )