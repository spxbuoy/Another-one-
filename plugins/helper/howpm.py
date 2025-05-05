from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("howpm"))
async def howpm(client, message):
    text = """<b>📊 PLAN COMPARISON - FREE VS PREMIUM
━━━━━━━━━━━━━━━━━━━━

[ϟ] STRIPE AUTH GATE (/cc)
  ● ANTISPAM:
    FREE - 15s | PREMIUM - 5s

[ϟ] STRIPE MASS AUTH GATE (/mass)
  ● ANTISPAM:
    FREE - 25s | PREMIUM - 10s
  ● LIMIT:
    FREE - 25 | PREMIUM - 50

[ϟ] SHOPIFY GATES (/sh, /ss1, /sf, /ho)
  ● ACCESS:
    FREE - Limited | PREMIUM - Full Access

[ϟ] CC GENERATOR (/gen)
  ● GENERATE LIMIT:
    FREE - 2000 | PREMIUM - 10000

━━━━━━━━━━━━━━━━━━━━</b>"""

    await message.reply_text(
        text,
        quote=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Back to Home", callback_data="commands")],
            [InlineKeyboardButton("Close", callback_data="close_ui")]
        ])
    )