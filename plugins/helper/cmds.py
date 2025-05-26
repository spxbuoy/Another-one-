from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# /cmds command opens the same menu as "Command Menu" button
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

# Callback handler: Command Menu
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

# Gate Menu
@Client.on_callback_query(filters.regex("open_gates"))
async def gates_menu(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "BARRY [GATES MENU]\n"
        "━━━━━━━━━━━━━\n"
        "Choose gate type:\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Auth Gates (2)\n"
        "[ϟ] Mass Checker (4)\n"
        "[ϟ] Shopify Gates (5)\n"
        "[ϟ] Charge Gates (2)",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Auth", callback_data="auth_menu"),
             InlineKeyboardButton("Mass Check", callback_data="mass")],
            [InlineKeyboardButton("Shopify", callback_data="shopify_menu"),
             InlineKeyboardButton("Charge", callback_data="charge_menu")],
            [InlineKeyboardButton("Back", callback_data="commands"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ])
    )

# Auth Menu
@Client.on_callback_query(filters.regex("auth_menu"))
async def auth_menu(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "BARRY [AUTH GATES]\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Braintree Auth\n"
        "[ϟ] Command: /b3 cc|mes|ano|cvv\n"
        "[ϟ] Status: Off ❌\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Stripe Auth\n"
        "[ϟ] Command: /cc cc|mes|ano|cvv\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: VBV Braintree\n"
        "[ϟ] Command: /vbv cc|mes|ano|cvv\n"
        "[ϟ] Status: Active ✅",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Back", callback_data="open_gates"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ])
    )

# Mass Menu
@Client.on_callback_query(filters.regex("mass"))
async def mass_check_gate(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "BARRY [MASS GATE MENU] (5 Gates)\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: M Stripe Auth Mass\n"
        "[ϟ] Command: /mass cc|mes|ano|cvv\n"
        "[ϟ] Status: Off ❌\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: M Stripe 1$ Charge\n"
        "[ϟ] Command: /mchk cc|mes|ano|cvv\n"
        "[ϟ] Status: Off ❌\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: M Shopify 0.99$\n"
        "[ϟ] Command: /msh cc|mes|ano|cvv\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: M Shopify 1.99$\n"
        "[ϟ] Command: /ms cc|mes|ano|cvv\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Mass Txt Shopify 1$\n"
        "[ϟ] Command: /mtxt (reply to .txt)\n"
        "[ϟ] Status: Active ✅\n",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Back", callback_data="open_gates"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ])
    )

# Shopify Menu
@Client.on_callback_query(filters.regex("shopify_menu"))
async def shopify_menu(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "BARRY [SHOPIFY GATES] (Page 1/2)\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Shopify 0.99$\n"
        "[ϟ] Command: /sh cc|mes|ano|cvv\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Shopify 2.47$\n"
        "[ϟ] Command: /ss1 cc|mes|ano|cvv\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Shopify 2$\n"
        "[ϟ] Command: /ho cc|mes|ano|cvv\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Shopify 5$\n"
        "[ϟ] Command: /sf cc|mes|ano|cvv\n"
        "[ϟ] Status: Active ✅\n",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➡️ Next", callback_data="shopify_page2")],
            [InlineKeyboardButton("Back", callback_data="open_gates"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ])
    )
   
@Client.on_callback_query(filters.regex("shopify_page2"))
async def shopify_menu_page2(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "BARRY [SHOPIFY GATES] (Page 2/2)\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: How to Add Auto Gate\n"
        "[ϟ] Command: /autoguide\n"
        "[ϟ] Status: Active ✅\n",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Back", callback_data="shopify_menu"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ])
    )


# Charge Menu
@Client.on_callback_query(filters.regex("charge_menu"))
async def charge_menu(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "BARRY [CHARGE GATES]\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Stripe 2$ Charge\n"
        "[ϟ] Command: /chk cc|mes|ano|cvv\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Clover 1$\n"
        "[ϟ] Command: /cl cc|mes|ano|cvv\n"
        "[ϟ] Status: Active ✅\n",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Back", callback_data="open_gates"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ])
    )

# Helper Menu
@Client.on_callback_query(filters.regex("open_helper"))
async def helper_menu(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "BARRY [HELPER MENU]\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Register\n"
        "[ϟ] Command: /register\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Credits Info\n"
        "[ϟ] Command: /howcrd\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Premium Info\n"
        "[ϟ] Command: /howpm\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Add Bot to Group\n"
        "[ϟ] Command: /howgp\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Buy Premium\n"
        "[ϟ] Command: /buy\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Report Bugs\n"
        "[ϟ] Command: /report\n"
        "[ϟ] Status: Off ❌\n"
        "━━━━━━━━━━━━━\n"
        "Total Commands: 6",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Back to Home", callback_data="commands"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ])
    )

# Tools Page 1
@Client.on_callback_query(filters.regex("open_tools"))
async def tools_menu_page1(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "BARRY [TOOLS PAGE 1/3]\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Bin Info\n"
        "[ϟ] Command: /bin\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: CC Gen\n"
        "[ϟ] Command: /gen bin\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: SK Checker\n"
        "[ϟ] Command: /sk sk_live_xxx\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Info\n"
        "[ϟ] Command: /info\n"
        "[ϟ] Status: Active ✅",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Next", callback_data="tools_page2")],
            [InlineKeyboardButton("Back to Home", callback_data="commands"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ])
    )

# Tools Page 2
@Client.on_callback_query(filters.regex("tools_page2"))
async def tools_menu_page2(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "BARRY [TOOLS PAGE 2/3]\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Ping\n"
        "[ϟ] Command: /ping\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: User ID\n"
        "[ϟ] Command: /id\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Credit Balance\n"
        "[ϟ] Command: /credits\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: CC Scraper\n"
        "[ϟ] Command: /scr channel 100\n"
        "[ϟ] Status: Active ✅",
        reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Next", callback_data="tools_page3")],
        [InlineKeyboardButton("Back", callback_data="open_tools"),
         InlineKeyboardButton("Close", callback_data="close_ui")]
    ])
 )
    
#Tool Page 3 
@Client.on_callback_query(filters.regex("tools_page3"))
async def tools_menu_page3(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "BARRY [TOOLS PAGE 3/3]\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: CC Cleaner Tool\n"
        "[ϟ] Command: /clean (reply to .txt)\n"
        "[ϟ] Status: Active ✅\n"
        "━━━━━━━━━━━━━\n"
        "[ϟ] Name: Sort CCs From Text\n"
        "[ϟ] Command: /sort (reply to message)\n"
        "[ϟ] Status: Active ✅",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Back", callback_data="tools_page2"),
             InlineKeyboardButton("Close", callback_data="close_ui")]
        ])
    )
