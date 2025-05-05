from pyrogram import Client, filters
from plugins.func.users_sql import plan_expirychk

@Client.on_message(filters.command('howgp'))
async def cmd_howgp(client, message):
    try:
        user_id = str(message.from_user.id)

        texta = (
            "𝗧𝗢 𝗔𝗗𝗗 𝗧𝗛𝗜𝗦 𝗕𝗢𝗧 𝗧𝗢 𝗬𝗢𝗨𝗥 𝗚𝗥𝗢𝗨𝗣 -\n\n"
            "⚠️ 𝗬𝗢𝗨𝗥 𝗚𝗥𝗢𝗨𝗣 𝗠𝗨𝗦𝗧 𝗛𝗔𝗩𝗘 𝗔𝗧 𝗟𝗘𝗔𝗦𝗧 𝟭𝟬𝟬+ 𝗠𝗘𝗠𝗕𝗘𝗥𝗦 ⚠️\n\n"
            "➤ 𝗔𝗗𝗗 𝗕𝗢𝗧: <b>@BarryxBot</b> 𝗧𝗢 𝗬𝗢𝗨𝗥 𝗚𝗥𝗢𝗨𝗣 𝗔𝗦 𝗔𝗗𝗠𝗜𝗡 (𝗗𝗢 𝗡𝗢𝗧 𝗚𝗜𝗩𝗘 𝗕𝗔𝗡 𝗣𝗘𝗥𝗠𝗜𝗦𝗦𝗜𝗢𝗡).\n"
            "➤ 𝗧𝗛𝗘𝗡 𝗔𝗗𝗗: <a href='tg://user?id=6440962840'>𝑩𝑨𝑹𝑹𝒀</a> 𝗧𝗢 𝗬𝗢𝗨𝗥 𝗚𝗥𝗢𝗨𝗣.\n"
            "➤ 𝗦𝗘𝗡𝗗 𝗬𝗢𝗨𝗥 𝗚𝗥𝗢𝗨𝗣 𝗖𝗛𝗔𝗧 𝗜𝗗 𝗧𝗢 𝗛𝗜𝗠 𝗙𝗢𝗥 𝗔𝗣𝗣𝗥𝗢𝗩𝗔𝗟.\n\n"
            "✅ 𝗢𝗡𝗖𝗘 𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗, 𝗬𝗢𝗨 𝗖𝗔𝗡 𝗨𝗦𝗘 𝗧𝗛𝗘 𝗕𝗢𝗧 𝗜𝗡 𝗬𝗢𝗨𝗥 𝗚𝗥𝗢𝗨𝗣!"
        )

        await message.reply_text(texta, reply_to_message_id=message.id)
        plan_expirychk(user_id)  # Removed await

    except Exception as e:
        await message.reply_text("❌ Error occurred.")
        print(f"/howgp error: {e}")