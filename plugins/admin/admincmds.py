from pyrogram import Client, filters

@Client.on_message(filters.command("adm", prefixes=["/", "."]))
async def cmd_adm(Client, message):
    user_id = str(message.from_user.id)
    CEO = "6440962840"

    if user_id != CEO:
        await message.reply_text("⚠️ <b>Requires Owner Privileges</b>", message.id)
    else:
        resp = f"""
<b>[ϟ] 𝗕𝗔𝗥𝗥𝗬 𝐁𝐎𝐓 𝐀𝐃𝐌𝐈𝐍 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒</b>
━━━━━━━━━━━━━━━━━━
[ϟ] <b>Auth a Group</b>  
➥ <code>/add -1002046472570</code>

[ϟ] <b>Unauth a Group</b>  
➥ <code>/del -1002046472570</code>

[ϟ] <b>Promote User</b>  
➥ <code>/pm 6440962840</code>

[ϟ] <b>Demote User</b>  
➥ <code>/fr 6440962840</code>

[ϟ] <b>Starter Plan</b>  
➥ <code>/sub1 6440962840</code>

[ϟ] <b>Silver Plan</b>  
➥ <code>/sub2 6440962840</code>

[ϟ] <b>Gold Plan</b>  
➥ <code>/sub3 6440962840</code>

[ϟ] <b>Custom Plan</b>  
➥ <code>/cs 6440962840</code>

[ϟ] <b>Generate Premium Giftcode</b>  
➥ <code>/gc 10</code>

[ϟ] <b>Give Credit to User</b>  
➥ <code>/ac 100 6440962840</code>

[ϟ] <b>Broadcast to All Users</b>  
➥ <code>/br Your message here</code>
━━━━━━━━━━━━━━━━━━
"""
        await message.reply_text(resp, message.id)