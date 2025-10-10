# config.py

API_ID = 22884130              # Telegram API ID
API_HASH = "a69e8b16dac958f1bd31eee360ec53fa"    # Telegram API hash
BOT_TOKEN = "8100230392:AAEO3UIwnfVPIfgs8KS-5MKsCsPEBiLu1mg"  # @BotFather token
MONGO_URI = "mongodb+srv://yoyat19687:byRateKzeofLw90e@cluster0.ysszzi9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
OWNER_ID = 8026801357

# Default Messages / Buttons (overridden by /settings)
DEFAULT_SETTINGS = {
    "start_pic": "",
    "start_msg": (
        "👋 **Hey {name}!**\n\n"
        "Welcome to the Contact Bot.\n"
        "You can use this bot to send messages directly to the admins.\n\n"
        "🪄 Use /contact to start chatting with the admin."
    ),
    "help_msg": (
        "🧭 **Help Menu**\n\n"
        "👤 **User Commands:**\n"
        "• /start - Start the bot\n"
        "• /contact - Send a message to admin\n\n"
        "🛠️ **Admin Commands:**\n"
        "• /addadmin <user_id>\n"
        "• /deladmin <user_id>\n"
        "• /admins - Show admin list\n"
        "• /users - Show total users\n"
        "• /reply <user_id> <msg>\n"
        "• /broadcast <msg>\n"
        "• /settings - Configure bot messages"
    )
}
