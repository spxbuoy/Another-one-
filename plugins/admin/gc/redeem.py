from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.func.users_sql import fetchinfo, updatedata
import sqlite3

@Client.on_message(filters.command("redeem"))
async def redeem_code(client, message: Message):
    try:
        user_id = message.from_user.id
        args = message.text.split()
        if len(args) != 2:
            return await message.reply_text("⚠️ Usage: <code>/redeem YOUR-CODE</code>", quote=True, )

        code = args[1].strip().upper()

        # Check if user is registered
        user_info = fetchinfo(user_id)
        if not user_info:
            return await message.reply_text("❌ You are not registered. Please use /register first.")

        # Connect DB
        conn = sqlite3.connect("plugins/xcc_db/users.db")
        c = conn.cursor()

        # Check code exists and not used
        c.execute("SELECT credits, status FROM keys WHERE code = ? AND used = 0", (code,))
        key_data = c.fetchone()

        if not key_data:
            return await message.reply_text("❌ Invalid or already used code.")

        credits_to_add = int(key_data[0])
        plan_type = key_data[1]

        # Mark code as used
        c.execute("UPDATE keys SET used = 1 WHERE code = ?", (code,))

        # Update user credits and plan
        current_info = fetchinfo(user_id)
        old_credits = int(current_info[5] or 0)
        new_credits = old_credits + credits_to_add

        updatedata(user_id, "credits", new_credits)
        updatedata(user_id, "plan", plan_type)

        # Optional: add counter
        try:
            current_total_keys = int(current_info[10] or 0)
            updatedata(user_id, "totalkey", current_total_keys + 1)
        except:
            pass  # skip if totalkey doesn't exist

        conn.commit()
        conn.close()

        await message.reply_text(
            f"✅ Successfully redeemed <code>{code}</code>\n"
            f"➕ Added {credits_to_add} credits\n"
            f"⭐ Plan upgraded to: <b>{plan_type}</b>",
            quote=True, 
        )

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}", quote=True)
