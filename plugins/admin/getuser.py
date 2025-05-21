from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import fetchinfo
from plugins.func.utils import error_log

OWNER_ID = "6440962840"  
@Client.on_message(filters.command("get", ["/", "."]))
async def cmd_get_userinfo(client: Client, message: Message):
    try:
        user_id = str(message.from_user.id)
        if user_id != OWNER_ID:
            return await message.reply_text("❌ You are not the bot owner.", quote=True)

      
        if message.reply_to_message:
            target_user_id = str(message.reply_to_message.from_user.id)
        else:
            args = message.text.split()
            if len(args) < 2:
                return await message.reply_text(
                    "<b>Usage:</b> <code>/get user_id</code>, <code>/get @username</code>, or reply to a user.",
                    quote=True
                )
            input_arg = args[1]
            if input_arg.startswith("@"):
                user_obj = await client.get_users(input_arg)
                target_user_id = str(user_obj.id)
            else:
                target_user_id = input_arg

        
        data = fetchinfo(target_user_id)
        if not data:
            return await message.reply_text(
                f"❌ No user found with ID or username: <code>{target_user_id}</code>",
                quote=True
            )

     
        _, username, status, plan, expiry, credits, _, _, _, reg_at, totalkey = data

        
        text = (
            f"𝗕𝗔𝗥𝗥𝗬 | {target_user_id} Info\n"
            f"━━━━━━━━━━━━━━\n"
            f"[ϟ] First Name : <a href='tg://user?id={target_user_id}'>{username}</a>\n"
            f"[ϟ] ID : <code>{target_user_id}</code>\n"
            f"[ϟ] Status : {status}\n"
            f"[ϟ] Plan : {plan}\n"
            f"[ϟ] Plan Expiry : {expiry}\n"
            f"[ϟ] Credit : {credits}\n"
            f"[ϟ] Keys Redeemed : {totalkey}\n"
            f"[ϟ] Registered At : {reg_at}\n"
            f"━━━━━━━━━━━━━━"
        )

        await message.reply_text(text, quote=True)

    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())
