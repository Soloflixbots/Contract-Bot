# Telegram API setup
API_ID = 123456               # Your Telegram API ID
API_HASH = "your_api_hash"    # Your Telegram API hash
BOT_TOKEN = "your_bot_token"  # Your bot token from @BotFather

# MongoDB setup
MONGO_URI = "your_mongodb_uri"  # Your MongoDB connection URI

# Bot settings
OWNER_ID = 123456789          # Your Telegram ID (owner)

# Start / Help customization
START_PIC = "https://telegra.ph/file/3cfd0a0ab8e1234567890.jpg"  # image link (can be from telegraph)
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
