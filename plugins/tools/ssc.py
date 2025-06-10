import asyncio, httpx, os
from io import StringIO
from pyrogram import Client, filters
from pyrogram.types import Message

sem = asyncio.Semaphore(20)

def format_result(site, item):
    return f"""<b>┏━━━━━━━⍟
┃Cheapest Product
┗━━━━━━━━━━━⊛</b>

⊙ <b>Product Variant:</b> {item.get('variant', 'N/A')}  
⊙ <b>Product Name:</b> {item['title']}  
⊙ <b>Product Price:</b> ${item['price']}  
⊙ <b>Product URL:</b> <code>{item['url']}</code>

<b>❛ ━━━━･⌁ 𝑩𝑨𝑹𝑹𝒀 ⌁･━━━━ ❜</b>"""

async def fetch_top_products(session, site):
    async with sem:
        try:
            if not site.startswith("http"):
                site = "https://" + site
            base_url = site.rstrip('/')
            products_url = base_url + "/products.json"

            r = await session.get(products_url, timeout=8)
            if r.status_code != 200:
                return f"❌ <b>{base_url}</b>\nFailed to fetch products."

            data = r.json()
            products = data.get("products", [])
            if not products:
                return f"❌ <b>{base_url}</b>\nNo products found."

            valid_items = []
            for product in products:
                handle = product.get("handle")
                for variant in product.get("variants", []):
                    try:
                        price = float(variant.get("price", "0.00"))
                        if price == 0.0:
                            continue
                        valid_items.append({
                            "title": product.get("title", "No Title"),
                            "price": price,
                            "url": f"{base_url}/products/{handle}",
                            "variant": variant.get("title", "Default Title")
                        })
                    except:
                        continue

            if not valid_items:
                return f"❌ <b>{base_url}</b>\nNo valid priced products."

            best_item = sorted(valid_items, key=lambda x: x["price"])[0]
            return format_result(base_url, best_item)

        except Exception as e:
            return f"❌ <b>{site}</b>\nError: <code>{str(e)}</code>"

@Client.on_message(filters.command("ssc", ["/", "."]))
async def ssc_cmd(client: Client, message: Message):
    args = message.text.split()
    if len(args) < 2:
        return await message.reply("❌ Usage:\n<code>/ssc site1 site2 ...</code>\nMax 10 sites.")

    sites = args[1:]
    if len(sites) > 10:
        return await message.reply("❌ You can check up to 10 sites at once.")

    m = await message.reply("🔍 Checking site(s)... Please wait ⌛")

    async with httpx.AsyncClient(follow_redirects=True) as session:
        tasks = [fetch_top_products(session, site) for site in sites]
        results = await asyncio.gather(*tasks)

    final_text = "\n\n".join(results)
    if len(final_text) > 4096:
        file = StringIO(final_text)
        file.name = "cheapest_results.txt"
        await message.reply_document(file, caption="📦 Cheapest Products List")
    else:
        await m.edit_text(final_text, disable_web_page_preview=True)

@Client.on_message(filters.command("sctxt", ["/", "."]))
async def sctxt_cmd(client: Client, message: Message):
    await message.reply("Reading site list... ⌛")
    sites = []

    if message.reply_to_message and message.reply_to_message.document:
        file = await message.reply_to_message.download()
        with open(file, "r") as f:
            sites = [line.strip() for line in f if line.strip()]
        os.remove(file)

    elif message.reply_to_message and message.reply_to_message.text:
        text = message.reply_to_message.text
        sites = [line.strip() for line in text.splitlines() if line.strip()]
    else:
        return await message.reply("❌ Reply to a .txt file or text list of Shopify sites.")

    async with httpx.AsyncClient(follow_redirects=True) as session:
        tasks = [fetch_top_products(session, site) for site in sites]
        results = await asyncio.gather(*tasks)

    final_text = "\n\n".join(results)
    if len(final_text) > 4096:
        file = StringIO(final_text)
        file.name = "cheapest_results.txt"
        await message.reply_document(file, caption="📦 Cheapest Products List")
    else:
        await message.reply(final_text, disable_web_page_preview=True)
