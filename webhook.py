import os
import requests
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# কনফিগারেশন
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_KEY = os.environ.get("API_KEY")

# ডেভেলপার ইনফো
DEVELOPER = "@codex_haseb"
BOT_NAME = "Number Lookup Bot"
CHANNEL_LINK = "https://t.me/codex_haseb_CHANNEL"
CHANNEL_USERNAME = "@codex_haseb_CHANNEL"  # চ্যানেলের ইউজারনেম

# স্টোরেজ
user_data_store = {}

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """চেক করে ব্যবহারকারী চ্যানেলের মেম্বার কিনা"""
    user_id = update.effective_user.id
    
    try:
        # টেলিগ্রাম API দিয়ে চেক করা
        chat_member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        
        if chat_member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except:
        return False

async def send_join_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """চ্যানেল জয়েন করার মেসেজ দেখায়"""
    keyboard = [
        [InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I HAVE JOINED", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = f"""
╭━━━━━━━━━━━━━━━━━━━━╮
┃  🔒 **ACCESS REQUIRED**  ┃
╰━━━━━━━━━━━━━━━━━━━━╯

⚠️ **You must join our channel first!**

📢 **Channel:** {CHANNEL_USERNAME}

━━━━━━━━━━━━━━━━━━━━
✅ **Benefits after joining:**
• Free Number Lookup
• Latest Updates
• 24/7 Bot Access
• Premium Features

━━━━━━━━━━━━━━━━━━━━
👇 **Click below to join:**
    """
    
    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """স্টার্ট কমান্ড - প্রথমে চ্যানেল চেক করে"""
    user_id = update.effective_user.id
    
    # চ্যানেল জয়েন চেক
    is_member = await check_membership(update, context)
    
    if not is_member:
        await send_join_message(update, context)
        return
    
    # মেম্বার হলে মেনু দেখান
    keyboard = [
        [InlineKeyboardButton("🛰️ GET INFO", callback_data="get_info")],
        [InlineKeyboardButton("🔍 LOOKUP NUMBER", callback_data="lookup")],
        [InlineKeyboardButton("📊 STATS", callback_data="stats")],
        [InlineKeyboardButton("👨‍💻 DEVELOPER", callback_data="developer")],
        [InlineKeyboardButton("ℹ️ ABOUT", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
╭━━━━━━━━━━━━━━━━━━╮
┃  ✨ **{BOT_NAME}** ✨
┃  🔍 Phone Number Info
╰━━━━━━━━━━━━━━━━━━╯

✅ **Channel Joined!** Thanks ❤️

📱 **Features:**
✅ Number Lookup
✅ Country Detection
✅ Carrier Info
✅ Fast Response

👨‍💻 **Developer:** {DEVELOPER}

👇 **Choose an option below**
    """
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """বাটন হ্যান্ডলার"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    # চ্যানেল জয়েন চেক (বাটন ক্লিকের সময়)
    if query.data != "check_join":
        is_member = await check_membership(update, context)
        if not is_member:
            await send_join_message(update, context)
            return
    
    if query.data == "check_join":
        # আবার চেক করা
        is_member = await check_membership(update, context)
        if is_member:
            await query.edit_message_text("✅ **Verification Successful!**\n\nWelcome to the bot! 🎉\n\nUse /start to continue.")
            # রিপ্লাই করার পর আবার মেনু দেখান
            keyboard = [
                [InlineKeyboardButton("🔄 START BOT", callback_data="restart")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "✅ **Welcome!** Click below to start:",
                reply_markup=reply_markup
            )
        else:
            await query.edit_message_text("❌ **Not Joined Yet!**\n\nPlease join the channel first:")
            await send_join_message(update, context)
    
    elif query.data == "restart":
        # বট রিস্টার্ট
        keyboard = [
            [InlineKeyboardButton("🛰️ GET INFO", callback_data="get_info")],
            [InlineKeyboardButton("🔍 LOOKUP NUMBER", callback_data="lookup")],
            [InlineKeyboardButton("📊 STATS", callback_data="stats")],
            [InlineKeyboardButton("👨‍💻 DEVELOPER", callback_data="developer")],
            [InlineKeyboardButton("ℹ️ ABOUT", callback_data="about")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "✨ **Bot Ready!**\n\nChoose an option:",
            reply_markup=reply_markup
        )
    
    elif query.data == "get_info":
        text = """
┏━━━━━━━━━━━━━━━━━━━━┓
┃  📱 **NUMBER LOOKUP**
┗━━━━━━━━━━━━━━━━━━━━┛

**Send the phone number:**

▫️ With country code: `88016xxxxxxxx`
▫️ Without +: `01648xxxxxx`

**Example:** `8801688888888`

⚡ _Powered by Lookup API_
        """
        await query.edit_message_text(
            text,
            parse_mode="Markdown"
        )
        user_data_store[user_id] = {'state': 'awaiting_number'}
    
    elif query.data == "lookup":
        text = """
🔍 **Quick Lookup**

Send the number you want to search:

📞 Format: `88016xxxxxxxx`
🌍 Example: `8801688888888`

*Include country code for best results*
        """
        await query.edit_message_text(
            text,
            parse_mode="Markdown"
        )
        user_data_store[user_id] = {'state': 'awaiting_number'}
    
    elif query.data == "stats":
        stats_text = f"""
📊 **Bot Statistics**

━━━━━━━━━━━━━━━━━
👥 **Users:** 1,234+
🔍 **Lookups:** 5,678+
✅ **Success Rate:** 98%
⚡ **Avg Response:** 2.1s
━━━━━━━━━━━━━━━━━

📢 **Channel:** {CHANNEL_USERNAME}
🆙 **Status:** Active
👨‍💻 **Dev:** {DEVELOPER}
        """
        keyboard = [[InlineKeyboardButton("🔄 REFRESH", callback_data="stats")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            stats_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    elif query.data == "developer":
        dev_text = f"""
👨‍💻 **Developer Information**

━━━━━━━━━━━━━━━━━━━
🌟 **Name:** HASEBUL HASAN
💬 **Username:** {DEVELOPER}
⚡ **Bot:** {BOT_NAME}
📅 **Version:** 2.0
━━━━━━━━━━━━━━━━━━━

🔧 **Skills:**
• Python | JavaScript
• Telegram API
• Web Development

📢 **Channel:** {CHANNEL_USERNAME}
💝 **Support Me:** {DEVELOPER}
        """
        keyboard = [
            [InlineKeyboardButton("💬 CONTACT", url=f"https://t.me/{DEVELOPER.replace('@', '')}")],
            [InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK)],
            [InlineKeyboardButton("🔙 BACK", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            dev_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    elif query.data == "about":
        about_text = f"""
ℹ️ **About {BOT_NAME}**

━━━━━━━━━━━━━━━━━━━
🔍 **Purpose:** Phone Number Information Lookup

🌍 **Supported:** Worldwide Numbers

📡 **API Source:** LookupNow.top

⚡ **Features:**
• Real-time lookup
• Carrier detection
• Country flag display
• Fast response

━━━━━━━━━━━━━━━━━━━
📢 **Channel:** {CHANNEL_USERNAME}
👨‍💻 **Developer:** {DEVELOPER}
        """
        keyboard = [
            [InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK)],
            [InlineKeyboardButton("🔙 BACK", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            about_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    elif query.data == "back_to_menu":
        await show_menu(query, user_id)

async def show_menu(query, user_id):
    """মেইন মেনু দেখায়"""
    keyboard = [
        [InlineKeyboardButton("🛰️ GET INFO", callback_data="get_info")],
        [InlineKeyboardButton("🔍 LOOKUP NUMBER", callback_data="lookup")],
        [InlineKeyboardButton("📊 STATS", callback_data="stats")],
        [InlineKeyboardButton("👨‍💻 DEVELOPER", callback_data="developer")],
        [InlineKeyboardButton("ℹ️ ABOUT", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    menu_text = f"""
╭━━━━━━━━━━━━━━━━━━╮
┃  ✨ **{BOT_NAME}** ✨
┃  🔍 Main Menu
╰━━━━━━━━━━━━━━━━━━╯

👋 Welcome back!

📢 **Channel:** {CHANNEL_USERNAME}

Choose an option below 👇
    """
    await query.edit_message_text(
        menu_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    if user_id in user_data_store:
        del user_data_store[user_id]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """মেসেজ হ্যান্ডলার"""
    user_id = update.effective_user.id
    
    # চ্যানেল জয়েন চেক
    is_member = await check_membership(update, context)
    if not is_member:
        await send_join_message(update, context)
        return
    
    message_text = update.message.text.strip()
    
    if user_id in user_data_store and user_data_store[user_id].get('state') == 'awaiting_number':
        # প্রসেসিং মেসেজ
        processing_msg = await update.message.reply_text(
            "⏳ **Processing...**\n\n🔍 Fetching information...",
            parse_mode="Markdown"
        )
        
        # API কল
        api_url = f"https://api.lookupnow.top/api/v1/query.php?key={API_KEY}&number={message_text}"
        
        try:
            response = requests.get(api_url, timeout=15)
            data = response.json()
            
            if data.get('status') == 'success' and data.get('data', {}).get('success'):
                api_data = data['data']
                
                # সুন্দর ফরম্যাটে রেজাল্ট
                result = f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━╮
┃  🔍 **LOOKUP RESULT**  ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━╯

📞 **Number:** `{api_data.get('number', 'N/A')}`
🌍 **Country:** {api_data.get('country', 'N/A')}
📡 **Carrier:** {api_data.get('carrier', 'N/A')}
👤 **Name:** {api_data.get('name', 'N/A')}
🆔 **Type:** {api_data.get('type', 'Mobile')}

━━━━━━━━━━━━━━━━━━━━━━━━
📅 **Time:** {api_data.get('timestamp', 'N/A')[:19]}
⚡ **Source:** {api_data.get('developer', 'API')}

📢 **Channel:** {CHANNEL_USERNAME}
👨‍💻 **Developer:** {DEVELOPER}
                """
                
                await processing_msg.delete()
                
                keyboard = [
                    [InlineKeyboardButton("🛰️ NEW LOOKUP", callback_data="get_info")],
                    [InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK)],
                    [InlineKeyboardButton("🔙 MAIN MENU", callback_data="back_to_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    result,
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
                
            else:
                await processing_msg.delete()
                error_text = """
❌ **Invalid Number!**

Please check the number and try again.

💡 **Tips:**
• Use international format
• Include country code
• Check number validity
                """
                keyboard = [[InlineKeyboardButton("🔄 TRY AGAIN", callback_data="get_info")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(error_text, reply_markup=reply_markup, parse_mode="Markdown")
                
        except Exception as e:
            await processing_msg.delete()
            error_text = f"""
❌ **Error Occurred!**

{str(e)[:80]}

Please try again with correct format.
            """
            keyboard = [[InlineKeyboardButton("🔄 RETRY", callback_data="get_info")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(error_text, reply_markup=reply_markup, parse_mode="Markdown")
        
        # স্টেট রিসেট
        if user_id in user_data_store:
            del user_data_store[user_id]
    
    else:
        # ডিফল্ট মেনু দেখান
        await start(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """হেল্প কমান্ড"""
    await start(update, context)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    return application

app = main()