from pyrogram import Client, filters
import requests
from plugins.func.users_sql import *
import asyncio

@Client.on_message(filters.command('sk'))
async def sk_gate(client, message):
    try:
        user_id = str(message.from_user.id)
        chat_id = str(message.chat.id)

        # Registration check
        regdata = fetchinfo(user_id)
        if regdata is None:
            return await message.reply_text(
                "𝗬𝗢𝗨 𝗔𝗥𝗘 𝗡𝗢𝗧 𝗥𝗘𝗚𝗜𝗦𝗧𝗘𝗥𝗘𝗗 ⚠️\n"
                "𝗨𝘀𝗲 /register 𝘁𝗼 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿."
            )
        plan_expirychk(user_id)
        status = regdata[2]

        # Group/personal restriction
        GROUP = open("plugins/group.txt").read().splitlines()
        if message.chat.type == "private" and status == "FREE":
            return await message.reply_text(
                "𝗙𝗥𝗘𝗘 𝗨𝗦𝗘𝗥𝗦 𝗖𝗔𝗡'𝗧 𝗨𝗦𝗘 𝗕𝗢𝗧 𝗜𝗡 𝗣𝗘𝗥𝗦𝗢𝗡𝗔𝗟 ❌"
            )
        if message.chat.type in ["group", "supergroup"] and str(chat_id) not in GROUP:
            return await message.reply_text("𝗨𝗡𝗔𝗨𝗧𝗛𝗢𝗥𝗜𝗭𝗘𝗗 𝗖𝗛𝗔𝗧 ❌")

        # Extract SK key (safe for Python <3.9)
        sk = (
            message.reply_to_message.text
            if message.reply_to_message
            else message.text[len("/sk "):].strip()
        )

        if not sk:
            return await message.reply_text("❌ Please reply with an SK key.")
        if not sk.startswith("sk_live"):
            return await message.reply_text("❌ Invalid format.\nSK key must start with <b>sk_live</b>.")

        # Animation steps
        step = await message.reply_text("𝐒𝐓𝐄𝐏 - 𝟏: 𝗩𝗲𝗿𝗶𝗳𝘆𝗶𝗻𝗴 𝗦𝗞 𝗞𝗲𝘆...")
        await asyncio.sleep(1)
        await step.edit_text("𝐒𝐓𝐄𝐏 - 𝟐: 𝗖𝗼𝗻𝗻𝗲𝗰𝘁𝗶𝗻𝗴 𝘁𝗼 𝗔𝗣𝗜...")
        await asyncio.sleep(1.2)
        await step.edit_text("𝐒𝐓𝐄𝐏 - 𝟑: 𝗖𝗵𝗲𝗰𝗸𝗶𝗻𝗴 𝗞𝗲𝘆 𝗦𝘁𝗮𝘁𝘂𝘀...")

        # Request to API
        url = f"https://sk.voidex.dev/getpk/{sk}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
        }
        res = requests.get(url, headers=headers)

        try:
            data = res.json()
        except Exception:
            return await step.edit_text(
                f"❌ Invalid API response:\n<code>{res.text.strip()}</code>"
            )

        # Handle response
        if "status" in data:
            if data["status"] == "live":
                title, result = "𝗟𝗜𝗩𝗘 𝗞𝗘𝗬 ✅", "SK LIVE 💚"
                await send_mtc(f"KEY: <code>{sk}</code>\n\nResult: {result}")
            elif data["status"] == "dead":
                title, result = "𝗗𝗘𝗔𝗗 𝗞𝗘𝗬 ❌", "DEAD KEY ❌"
            else:
                title, result = "𝗨𝗡𝗞𝗡𝗢𝗪𝗡 ❓", data.get("message", "Unknown")
        elif "error" in data:
            title, result = "𝗗𝗘𝗔𝗗 𝗞𝗘𝗬 ❌", data["error"]
        else:
            title, result = "𝗘𝗥𝗥𝗢𝗥 ❌", f"Unexpected response:\n{res.text.strip()}"

        # Final styled output
        await step.edit_text(
            f"{title}\n\n"
            f"<b>𝗞𝗘𝗬:</b> <code>{sk}</code>\n"
            f"<b>𝗦𝗧𝗔𝗧𝗨𝗦:</b> {result}\n\n"
            f"𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆: <a href=\"tg://user?id={user_id}\">{message.from_user.first_name}</a> [ {status} ]\n"
            f"𝗕𝗼𝘁 𝗕𝘆: <a href=\"tg://user?id=6440962840\">𝑩𝑨𝑹𝑹𝒀</a>"
        )

    except Exception as e:
        await message.reply_text(f"❌ Error:\n<code>{e}</code>")