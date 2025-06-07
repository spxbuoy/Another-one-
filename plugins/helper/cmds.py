from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# Main linked icon
linked_ϟ = '<a href="https://t.me/+CUKFuQJYJTUwZmU8">ϟ</a>'

@Client.on_message(filters.command("cmds", prefixes=["/", "."]))
async def command_root_menu(client, message):
    await message.reply_text(
        "BARRY [COMMAND CENTER]\n━━━━━━━━━━━━━\nSelect a section to explore:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Gate", callback_data="open_gates"),
             InlineKeyboardButton("Tools", callback_data="open_tools")],
            [InlineKeyboardButton("Helper", callback_data="open_helper")],
            [InlineKeyboardButton("Close", callback_data="close_ui")]
        ])
    )

@Client.on_callback_query(filters.regex("commands"))
async def commands_callback(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "BARRY [COMMAND CENTER]\n━━━━━━━━━━━━━\nSelect a section to explore:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Gate", callback_data="open_gates"),
             InlineKeyboardButton("Tools", callback_data="open_tools")],
            [InlineKeyboardButton("Helper", callback_data="open_helper")],
            [InlineKeyboardButton("Close", callback_data="close_ui")]
        ])
    )
@Client.on_callback_query(filters.regex("open_gates"))
async def gates_menu(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        f"BARRY [GATES MENU]\n"
        f"━━━━━━━━━━━━━\n"
        f"Choose gate type:\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Auth Gates (2)\n"
        f"[{linked_ϟ}] Mass Checker (6)\n"
        f"[{linked_ϟ}] Shopify Gates (6)\n"
        f"[{linked_ϟ}] Charge Gates (2)",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Auth", callback_data="auth_menu"),
             InlineKeyboardButton("Mass Check", callback_data="mass")],
            [InlineKeyboardButton("Shopify", callback_data="shopify_menu"),
             InlineKeyboardButton("Charge", callback_data="charge_menu")],
            [InlineKeyboardButton("Back", callback_data="commands"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ]),
        
    )
@Client.on_callback_query(filters.regex("auth_menu"))
async def auth_menu(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        f"BARRY [AUTH GATES]\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Braintree Auth\n"
        f"[{linked_ϟ}] Command: /b3 cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Off ❌\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Stripe Auth\n"
        f"[{linked_ϟ}] Command: /cc cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: VBV Braintree\n"
        f"[{linked_ϟ}] Command: /vbv cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Active ✅",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Back", callback_data="open_gates"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ]),
    )
@Client.on_callback_query(filters.regex("auth_menu"))
async def auth_menu(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        f"BARRY [AUTH GATES]\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Braintree Auth\n"
        f"[{linked_ϟ}] Command: /b3 cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Off ❌\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Stripe Auth\n"
        f"[{linked_ϟ}] Command: /cc cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: VBV Braintree\n"
        f"[{linked_ϟ}] Command: /vbv cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Active ✅",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Back", callback_data="open_gates"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ]),
        
    )
@Client.on_callback_query(filters.regex("^mass$"))
async def mass_check_gate(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        f"BARRY [MASS GATE MENU] (Page 1/2)\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: M Stripe Auth Mass\n"
        f"[{linked_ϟ}] Command: /mass cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: M Stripe 1$ Charge\n"
        f"[{linked_ϟ}] Command: /mchk cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Off ❌\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: M Shopify 0.99$\n"
        f"[{linked_ϟ}] Command: /msh cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: M Shopify 1.99$\n"
        f"[{linked_ϟ}] Command: /ms cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Active ✅\n",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➡️ Next", callback_data="mass_page2")],
            [InlineKeyboardButton("Back", callback_data="open_gates"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ]),
        
    )

@Client.on_callback_query(filters.regex("mass_page2"))
async def mass_check_gate_page2(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        f"BARRY [MASS GATE MENU] (Page 2/2)\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Mass Txt Shopify 2$\n"
        f"[{linked_ϟ}] Command: /mtxt (reply to .txt)\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: M Shopify 0.80$\n"
        f"[{linked_ϟ}] Command: /msf cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Active ✅\n",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Back", callback_data="mass")],
            [InlineKeyboardButton("Back to Menu", callback_data="open_gates"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ]),
        
    )
@Client.on_callback_query(filters.regex("shopify_menu"))
async def shopify_menu(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        f"BARRY [SHOPIFY GATES] (Page 1/2)\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Shopify 0.99$\n"
        f"[{linked_ϟ}] Command: /sh cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Shopify 2.47$\n"
        f"[{linked_ϟ}] Command: /ss1 cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Shopify 3$\n"
        f"[{linked_ϟ}] Command: /ho cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Shopify 5$\n"
        f"[{linked_ϟ}] Command: /sf cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Active ✅\n",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➡️ Next", callback_data="shopify_page2")],
            [InlineKeyboardButton("Back", callback_data="open_gates"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ]),
        
    )

@Client.on_callback_query(filters.regex("shopify_page2"))
async def shopify_menu_page2(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        f"BARRY [SHOPIFY GATES] (Page 2/2)\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: How to Add Auto Gate\n"
        f"[{linked_ϟ}] Command: /autoguide\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Shopify 0.98$\n"
        f"[{linked_ϟ}] Command: /as cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Active ✅\n",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Back", callback_data="shopify_menu"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ]),
        
    )
@Client.on_callback_query(filters.regex("charge_menu"))
async def charge_menu(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        f"BARRY [CHARGE GATES]\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Stripe 2$ Charge\n"
        f"[{linked_ϟ}] Command: /chk cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Off ❌\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Clover 1$\n"
        f"[{linked_ϟ}] Command: /cl cc|mes|ano|cvv\n"
        f"[{linked_ϟ}] Status: Off ❌\n",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Back", callback_data="open_gates"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ]),
        
    )
@Client.on_callback_query(filters.regex("open_helper"))
async def helper_menu(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        f"BARRY [HELPER MENU]\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Register\n"
        f"[{linked_ϟ}] Command: /register\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Credits Info\n"
        f"[{linked_ϟ}] Command: /howcrd\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Premium Info\n"
        f"[{linked_ϟ}] Command: /howpm\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Add Bot to Group\n"
        f"[{linked_ϟ}] Command: /howgp\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Buy Premium\n"
        f"[{linked_ϟ}] Command: /buy\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Report Bugs\n"
        f"[{linked_ϟ}] Command: /report\n"
        f"[{linked_ϟ}] Status: Off ❌\n"
        "━━━━━━━━━━━━━\n"
        "Total Commands: 6",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Back to Home", callback_data="commands"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ]),
        
    )
@Client.on_callback_query(filters.regex("open_tools"))
async def tools_menu_page1(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        f"BARRY [TOOLS PAGE 1/3]\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Bin Info\n"
        f"[{linked_ϟ}] Command: /bin\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: CC Gen\n"
        f"[{linked_ϟ}] Command: /gen bin\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: SK Checker\n"
        f"[{linked_ϟ}] Command: /sk sk_live_xxx\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Info\n"
        f"[{linked_ϟ}] Command: /info\n"
        f"[{linked_ϟ}] Status: Active ✅",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Next", callback_data="tools_page2")],
            [InlineKeyboardButton("Back to Home", callback_data="commands"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ]),
        
    )
@Client.on_callback_query(filters.regex("tools_page2"))
async def tools_menu_page2(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        f"BARRY [TOOLS PAGE 2/3]\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Ping\n"
        f"[{linked_ϟ}] Command: /ping\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: User ID\n"
        f"[{linked_ϟ}] Command: /id\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Credit Balance\n"
        f"[{linked_ϟ}] Command: /credits\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: CC Scraper\n"
        f"[{linked_ϟ}] Command: /scr channel 100\n"
        f"[{linked_ϟ}] Status: Active ✅",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Next", callback_data="tools_page3")],
            [InlineKeyboardButton("Back", callback_data="open_tools"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ]),
        
    )
@Client.on_callback_query(filters.regex("tools_page3"))
async def tools_menu_page3(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        f"BARRY [TOOLS PAGE 3/3]\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: CC Cleaner Tool\n"
        f"[{linked_ϟ}] Command: /clean (reply to .txt)\n"
        f"[{linked_ϟ}] Status: Active ✅\n"
        f"━━━━━━━━━━━━━\n"
        f"[{linked_ϟ}] Name: Sort CCs From Text\n"
        f"[{linked_ϟ}] Command: /sort (reply to message)\n"
        f"[{linked_ϟ}] Status: Active ✅",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Back", callback_data="tools_page2"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ]),
        
    )
