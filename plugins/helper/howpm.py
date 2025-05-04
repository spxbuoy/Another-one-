from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("howpm"))
async def howpm(client, message):
    text = """<b>📊 PLAN COMPARISON - FREE VS PREMIUM VS PAID
━━━━━━━━━━━━━━━━━━━━

[ϟ] STRIPE AUTH GATE (/cc)
  ● ANTISPAM:
    FREE - 30s | PREMIUM - 5s | PAID - 5s

[ϟ] STRIPE MASS AUTH GATE (/mass)
  ● ANTISPAM:
    FREE - 120s | PREMIUM - 80s | PAID - 30s
  ● LIMIT:
    FREE - 8 | PREMIUM - 15 | PAID - 25

[ϟ] CC SCRAPER (/scr)
  ● SCRAPE LIMIT:
    FREE - 3000 | PREMIUM - 6000 | PAID - 12000

[ϟ] CC GENERATOR (/gen)
  ● GENERATE LIMIT:
    FREE - 2000 | PREMIUM - 4000 | PAID - 10000
━━━━━━━━━━━━━━━━━━━━</b>"""

    await message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Back to Home", callback_data="commands")],
            [InlineKeyboardButton("Close", callback_data="close_ui")]
        ])
    )