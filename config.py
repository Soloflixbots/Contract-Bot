# Telegram API setup
API_ID = 22884130               # Your Telegram API ID
API_HASH = "a69e8b16dac958f1bd31eee360ec53fa"    # Your Telegram API hash
BOT_TOKEN = "8100230392:AAEO3UIwnfVPIfgs8KS-5MKsCsPEBiLu1mg"  # Your bot token from @BotFather

# MongoDB setup
MONGO_URI = "mongodb+srv://yoyat19687:byRateKzeofLw90e@cluster0.ysszzi9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Your MongoDB connection URI

# Bot settings
OWNER_ID = 8026801357         # Your Telegram ID (owner)

# Start / Help customization
START_PIC = "https://graph.org/file/ebec9517dcb8ce2645ee6-f78863ff31185ca41b.jpg"  # image link (can be from telegraph)
START_MSG = (
    "👋 **Hey {name}!**\n\n"
    "Welcome to the Contact Bot.\n"
    "You can use this bot to send messages directly to the admins or owner.\n\n"
    "🪄 Use /contact to start chatting with the admin."
)

HELP_MSG = (
    "🧭 **Help Menu**\n\n"
    "Here are the commands you can use:\n\n"
    "👤 **User Commands:**\n"
    "• /start - Start the bot\n"
    "• /contact - Send a message to admin\n\n"
    "🛠️ **Admin Commands:**\n"
    "• /addadmin <user_id> - Add new admin\n"
    "• /deladmin <user_id> - Remove admin\n"
    "• /admins - Show admin list\n"
    "• /broadcast <msg> - Send broadcast to all users\n\n"
    "💬 Users’ messages will be forwarded to admins automatically."
)
