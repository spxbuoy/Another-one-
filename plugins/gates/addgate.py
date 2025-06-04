from pyrogram import Client, filters
from plugins.func.users_sql import set_user_gate

@Client.on_message(filters.command("addgate", ["/", "."]))
async def add_gate_cmd(client, message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            return await message.reply_text("❌ Usage: /addgate <site_url> [proxy]", quote=True)

        site_url = parts[1]
        proxy = parts[2] if len(parts) > 2 else None
        user_id = str(message.from_user.id)

        set_user_gate(user_id, site_url, proxy)

        cmd_name = site_url.strip("/").split("/")[-1][:8].lower()
        return await message.reply_text(
            f"✅ Shopify command has been created.\n\n"
            f"<b>Site:</b> {site_url}\n"
            f"<b>Proxy:</b> {proxy or 'None'}",
            quote=True
        )

    except Exception as e:
        await message.reply_text(f"❌ Error:\n<code>{str(e)}</code>", quote=True)