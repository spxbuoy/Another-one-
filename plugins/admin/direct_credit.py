from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import fetchinfo, updatedata

CEO_ID = 6440962840  # Replace with your actual Telegram user ID

@Client.on_message(filters.command("ac"))
async def cmd_ac(client: Client, message: Message):
    if message.from_user.id != CEO_ID:
        await message.reply_text(
            "❌ Requires Owner Privileges.",
            quote=True
        )
        return

    try:
        _, amt_str, user_id = message.text.split(maxsplit=2)
        amt = int(amt_str)

        fetch = fetchinfo(user_id)
        if not fetch:
            await message.reply_text("❌ User not found in database.", quote=True)
            return

        current_credit = int(fetch[5])
        new_credit = current_credit + amt

        updatedata(user_id, "credit", new_credit)

        await message.reply_text(
            f"<code>{amt}</code> credits successfully added to <a href='tg://user?id={user_id}'>{user_id}</a> ✅",
            quote=True,
            parse_mode="html"
        )

        await client.send_message(
            int(user_id),
            f"🎉 <b>Credits Added!</b>\n\n"
            f"You received <code>{amt}</code> new credits.\n"
            f"Use <code>/credits</code> to check your balance.",
            parse_mode="html"
        )

    except ValueError:
        await message.reply_text("⚠️ Usage: <code>/ac amount user_id</code>", quote=True, parse_mode="html")
    except Exception as e:
        await message.reply_text(f"❌ Error: <code>{e}</code>", quote=True, parse_mode="html")