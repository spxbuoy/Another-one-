from pyrogram import Client, filters

@Client.on_message(filters.command ('chk'))
async def cmd_start(client,message):
  await message.reply_text("Gate is currently off ⚠️",message.id)
