from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import fetchinfo, updatedata

CEO_ID = 6440962840  # Replace with your actual Telegram user ID

@Client.on_message(filters.command("ac", prefixes=["/", "."]))
async def cmd_ac(client: Client, message: Message):
    if message.from_user.id != CEO_ID:
        await message.reply_text(
            "❌ Requires Owner Privileges.",
            quote=True
        )
        return

    try:
        args = message.text.split(maxsplit=2)
        if len(args) != 3:
            await message.reply_text("⚠️ Usage: <code>/ac amount user_id</code>", quote=True)
            return
        
        _, amt_str, user_id = args
        amt = int(amt_str)

        # Fetch user info from database (non-async)
        fetch = fetchinfo(user_id)
        if not fetch:
            await message.reply_text("❌ User not found in database.", quote=True)
            return

        # Handle None or missing credits
        current_credit = int(fetch[5] or 0)
        new_credit = current_credit + amt

        # Update the credits in the database (non-async)
        updatedata(user_id, "credits", new_credit)

        # Notify CEO
        await message.reply_text(
            f"<code>{amt}</code> credits successfully added to <a href='tg://user?id={user_id}'>{user_id}</a> ✅",
            quote=True
        )

        # Notify the user
        try:
            await client.send_message(
                int(user_id),
                f"🎉 <b>Credits Added!</b>\n\n"
                f"You received <code>{amt}</code> new credits.\n"
                f"Use <code>/credits</code> to check your balance.",
            )
        except:
            pass  # User might have blocked the bot

    except ValueError:
        await message.reply_text("⚠️ Usage: <code>/ac amount user_id</code>", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: <code>{e}</code>", quote=True)
        print(f"Error in /ac command: {e}")