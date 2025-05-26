from pyrogram import Client, filters

@Client.on_message(filters.command("autoguide", prefixes=["/", "."]) & filters.private)
async def show_auto_gate_guide(client, message):
    text = """✅ <b>Auto Gate Successfully Added!</b>

🔹 <b>To add a gate, use this command format:</b>
<code>/addsh url=[your-url] name=[Your_Cmds_Name] command=[Your_Cmds] shipping=[True/False]</code>

📘 <b>Example:</b>
<code>/addsh url=https://yourshop.com/product/x name=MyGate command=mygatecmd shipping=False</code>

📌 <b>Parameters Explained:</b>
- <code>url</code> – The product or service link.
- <code>name</code> – A friendly name for your gate.
- <code>command</code> – The trigger command (e.g., /mygatecmd).
- <code>shipping</code> – Set to <code>True</code> if shipping is required, else <code>False</code>.

🗑️ <b>To delete a gate, use:</b>
<code>/dgate [your_cmd]</code>

👁️ <b>To view all your gates, type:</b>
<code>/mygate</code>
"""
    await message.reply_text(text, )
