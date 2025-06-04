from pyrogram import Client, filters
from plugins.func.users_sql import get_all_custom_gates

@Client.on_message((filters.command("mygates") | filters.regex(r"^\.mygates")) & filters.private)
async def show_my_commands(client, message):
    gates = get_all_custom_gates(message.from_user.id)
    if not gates:
        await message.reply("❌ You haven't added any gate commands yet.")
        return

    text = "🧾 Your Gate Commands:\n\n"
    for command, url, name, shipping in gates:
        text += f"{command} — {name}\nURL: {url}\nShipping: {shipping}\n\n"

    await message.reply(text)
