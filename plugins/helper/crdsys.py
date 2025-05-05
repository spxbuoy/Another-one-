from pyrogram import Client, filters
from plugins.func.users_sql import plan_expirychk

@Client.on_message(filters.command("howcrd"))
async def cmd_howcrd(client, message):
    try:
        user_id = str(message.from_user.id)

        text = (
            "𝗕𝗔𝗥𝗥𝗬 [𝗖𝗥𝗘𝗗𝗜𝗧 𝗦𝗬𝗦𝗧𝗘𝗠]\n"
            "━━━━━━━━━━━━━\n"
            "➤ 𝙰𝚄𝚃𝙷 𝙶𝙰𝚃𝙴𝚂\n"
            "➤ 1 Credit per CC Check\n"
            "━━━━━━━━━━━━━\n"
            "➤ 𝙲𝙷𝙰𝚁𝙶𝙴 𝙶𝙰𝚃𝙴𝚂\n"
            "➤ 1 Credit per CC Check\n"
            "━━━━━━━━━━━━━\n"
            "➤ 𝙼𝙰𝚂𝚂 𝙰𝚄𝚃𝙷 𝙶𝙰𝚃𝙴𝚂\n"
            "➤ 1 Credit per CC\n"
            "━━━━━━━━━━━━━\n"
            "➤ 𝙼𝙰𝚂𝚂 𝙲𝙷𝙰𝚁𝙶𝙴 𝙶𝙰𝚃𝙴𝚂\n"
            "➤ 1 Credit per CC\n"
            "━━━━━━━━━━━━━\n"
            "➤ 𝚂𝙷𝙾𝙿𝙸𝙵𝚈 𝙲𝙷𝙴𝙲𝙺\n"
            "➤ 1 Credit per Check\n"
            "━━━━━━━━━━━━━"
        )

        await message.reply_text(text, reply_to_message_id=message.id)
        plan_expirychk(user_id)  # Fixed: removed `await`

    except Exception as e:
        await message.reply_text("❌ Error while showing credit system.")
        print(f"/howcrd error: {e}")