# ==========================
#   CONTACT BOT CONFIG FILE
# ==========================

# --- Telegram API Setup ---
API_ID = 22884130
API_HASH = "a69e8b16dac958f1bd31eee360ec53fa"
BOT_TOKEN = "8489912478:AAGgN13yEVcFhu6oJDsPJ8927q7XF6qB6Cs"

# --- MongoDB Setup ---
MONGO_URI = (
    "mongodb+srv://yoyat19687:byRateKzeofLw90e@cluster0.ysszzi9.mongodb.net/"
    "?retryWrites=true&w=majority&appName=Cluster0"
)

# --- Owner Settings ---
OWNER_ID = 8026801357  # Your Telegram ID

# --- Start / Help Customization ---
START_PIC = "https://telegra.ph/file/ebec9517dcb8ce2645ee6.jpg"  # ✅ direct .jpg link
LOCAL_START_PIC = "start.jpg"  # fallback local file

START_MSG = (
    "👋 **Hey {name}!**\n\n"
    "Welcome to the **Contact Bot** 💬\n"
    "You can use this bot to send messages directly to admins or the owner.\n\n"
    "🪄 Use the button below or type /contact to send your first message!"
)

HELP_MSG = (
    "🧭 **Help Menu**\n\n"
    "👤 **User Commands:**\n"
    "• /start - Start the bot\n"
    "• /contact - Send a message to admin\n\n"
    "🛠️ **Admin Commands:**\n"
    "• /addadmin <user_id>\n"
    "• /deladmin <user_id>\n"
    "• /admins - Show admin list\n"
    "• /users - Show total users\n"
    "• /reply <user_id> <message> - Reply to a user\n"
    "• /broadcast <message> - Send message to all users\n"
    "• /settings - Configure bot messages"
)
