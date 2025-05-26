from pyrogram import Client, filters
from plugins.func.users_sql import save_custom_gate

@Client.on_message((filters.command("addsh") | filters.regex(r"^\.addsh")) & filters.private)
async def addsh(client, message):
    if len(message.text.split()) == 1:
        await message.reply(
            "Example usage:\n"
            "command = test\n"
            "name = cool gate\n"
            "shipping = True\n"
            "url = https://example.com/product/hello"
        )
        return

    try:
        text = message.text.split(" ", 1)[1]
        parts = text.split()
        data = {}

        for p in parts:
            if "=" in p:
                key, value = p.split("=", 1)
                data[key.lower()] = value.strip()

        url = data.get("url")
        name = data.get("name", "Gate")
        command = data.get("command")
        shipping = data.get("shipping", "False").strip().lower() == "true"

        if not url or not command:
            await message.reply("❌ Format error. Required: url= command= ")
            return

        #if not command.startswith("/"):
#            command = "/" + command

        
        save_custom_gate(
            user_id=message.from_user.id,
            command=command,
            site_url=url,
            gate_name=name,
            shipping=str(shipping)
        )

        await message.reply(
            f"✅ Gate added:\n"
            f"Command: {command}\n"
            f"Name: {name}\n"
            f"Shipping: {shipping}\n"
            f"URL: {url}"
        )

    except Exception as e:
        await message.reply(f"❌ Error adding gate:\n{e}")
