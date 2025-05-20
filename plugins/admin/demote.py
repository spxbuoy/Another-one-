from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import fetchinfo, updatedata

CEO_ID = 6440962840  # Owner ID as integer

@Client.on_message(filters.command("fr", prefixes=["/", "."]))
async def cmd_fr(client: Client, message: Message):
    if message.from_user.id != CEO_ID:
        await message.reply_text("𝗥𝗲𝗾𝘂𝗶𝗿𝗲 𝗢𝘄𝗻𝗲𝗿 𝗣𝗿𝗶𝘃𝗶𝗹𝗮𝗴𝗲𝘀 ⚠️", quote=True)
        return

    try:
        # Determine target user
        if message.reply_to_message:
            target_user_id = message.reply_to_message.from_user.id
        else:
            try:
                target_user_id = int(message.text.split(maxsplit=1)[1])
            except IndexError:
                await message.reply_text("𝗨𝘀𝗲𝗴𝗲: <code>/fr user_id</code> or reply to a user", quote=True)
                return

        user_data = fetchinfo(target_user_id)
        status = str(user_data[2]) if user_data else "UNKNOWN"

        if status != "PREMIUM":
            await message.reply_text(
                f"<a href='tg://user?id={target_user_id}'>{target_user_id}</a> 𝗶𝘀 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗮 𝗙𝗥𝗘𝗘 𝗠𝗲𝗺𝗯𝗲𝗿 ⚠️.",
                quote=True
            )
        else:
            updatedata(target_user_id, "status", "FREE")
            await message.reply_text(
                f"<a href='tg://user?id={target_user_id}'>{target_user_id}</a> 𝗶𝘀 𝗗𝗘𝗠𝗢𝗧𝗘𝗗 𝘁𝗼 𝗮 𝗙𝗥𝗘𝗘 𝗠𝗲𝗺𝗯𝗲𝗿 ✅.",
                quote=True
            )

            await client.send_message(
                target_user_id,
                "𝗛𝗘𝗬 𝗗𝗨𝗗𝗘!\n𝗬𝗢𝗨𝗥 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗛𝗔𝗦 𝗕𝗘𝗘𝗡 𝗗𝗘𝗠𝗢𝗧𝗘𝗗 𝗧𝗢 '𝗙𝗥𝗘𝗘' 𝗨𝗦𝗘𝗥 ✅"
            )
    except Exception as e:
        await message.reply_text(f"❌ Error: <code>{e}</code>", quote=True)