from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import fetchinfo
from plugins.func.utils import error_log

OWNER_ID = "6440962840"

@Client.on_message(filters.command("get", ["/", "."]))
async def cmd_get_userinfo(client: Client, message: Message):
    try:
        if not message.from_user:
            return await message.reply_text("❌ Could not identify sender.")

        user_id = str(message.from_user.id)
        if user_id != OWNER_ID:
            return await message.reply_text("❌ You are not the bot owner.", quote=True)

        if message.reply_to_message and message.reply_to_message.from_user:
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
                try:
                    user_obj = await client.get_users(input_arg)
                    target_user_id = str(user_obj.id)
                except Exception as e:
                    return await message.reply_text(f"❌ Failed to fetch user: {e}", quote=True)
            else:
                target_user_id = input_arg

        data = fetchinfo(target_user_id)
        if not data:
            return await message.reply_text(
                f"❌ No user found with ID or username: <code>{target_user_id}</code>",
                quote=True
            )

        username = data[1] if len(data) > 1 else "N/A"
        status = data[2] if len(data) > 2 else "N/A"
        plan = data[3] if len(data) > 3 else "N/A"
        expiry = data[4] if len(data) > 4 else "N/A"
        credits = data[5] if len(data) > 5 else "0"
        reg_at = data[9] if len(data) > 9 else "Unknown"
        totalkey = data[10] if len(data) > 10 else "0"

        # Make [ϟ] clickable
        linked_ϟ = '<a href="https://t.me/+CUKFuQJYJTUwZmU8">ϟ</a>'

        text = (
            f"𝗕𝗔𝗥𝗥𝗬 | {target_user_id} Info\n"
            f"━━━━━━━━━━━━━━\n"
            f"[{linked_ϟ}] First Name : <a href='tg://user?id={target_user_id}'>{username}</a>\n"
            f"[{linked_ϟ}] ID : <code>{target_user_id}</code>\n"
            f"[{linked_ϟ}] Status : {status}\n"
            f"[{linked_ϟ}] Plan : {plan}\n"
            f"[{linked_ϟ}] Plan Expiry : {expiry}\n"
            f"[{linked_ϟ}] Credit : {credits}\n"
            f"[{linked_ϟ}] Keys Redeemed : {totalkey}\n"
            f"[{linked_ϟ}] Registered At : {reg_at}\n"
            f"━━━━━━━━━━━━━━"
        )

        await message.reply_text(text, quote=True)

    except Exception as e:
        import traceback
        err = traceback.format_exc()
        await error_log(err)
        await message.reply_text(f"❌ An error occurred:\n<code>{e}</code>", quote=True)
