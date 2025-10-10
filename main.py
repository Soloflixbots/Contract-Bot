from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI, ADMINS, START_PIC, HELP_PIC

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["contact_bot"]
users_col = db["users"]

# Initialize bot
bot = Client("contact_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# start
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    users_col.update_one(
        {"user_id": message.from_user.id},
        {"$set": {"user_id": message.from_user.id, "first_name": message.from_user.first_name}},
        upsert=True
    )
    text = "👋 Hey there! Welcome to the Contact Bot.\n\nUse /help to see commands."
    await message.reply_photo(photo=START_PIC, caption=text)

# /help
@bot.on_message(filters.command("help") & filters.private)
async def help_msg(client, message):
    text = (
        "🛠️ Commands available:\n\n"
        "👤 User Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n\n"
        "🛡️ Admin Commands:\n"
        "/reply - Reply to a user\n"
        "/broadcast - Broadcast message\n"
        "/users - Show total users\n"
        "/add_admin - Add admin\n"
        "/rev_admin - Remove admin"
    )
    await message.reply_photo(photo=HELP_PIC, caption=text)
    
# Reply command (admin only)
@bot.on_message(filters.command("reply") & filters.user(ADMINS))
async def reply_msg(client, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a user's message with /reply <text>")
        return
    parts = message.text.split(None, 1)
    if len(parts) < 2:
        await message.reply_text("Provide a message to send.")
        return
    await message.reply_to_message.reply_text(parts[1])
    await message.reply_text("✅ Message sent!")

# Broadcast command (admin only)
@bot.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def broadcast_msg(client, message):
    parts = message.text.split(None, 1)
    if len(parts) < 2:
        await message.reply_text("Provide a message to broadcast.")
        return
    users = users_col.find({})
    success = 0
    for user in users:
        try:
            await bot.send_message(user["user_id"], parts[1])
            success += 1
        except:
            continue
    await message.reply_text(f"✅ Broadcast sent to {success} users!")

# Users command (admin only)
@bot.on_message(filters.command("users") & filters.user(ADMINS))
async def total_users(client, message):
    count = users_col.count_documents({})
    await message.reply_text(f"👥 Total users: {count}")

# Add admin command
@bot.on_message(filters.command("add_admin") & filters.user(ADMINS))
async def add_admin(client, message):
    parts = message.text.split(None, 1)
    if len(parts) < 2:
        await message.reply_text("Send /add_admin <user_id>")
        return
    try:
        new_admin = int(parts[1])
        if new_admin not in ADMINS:
            ADMINS.append(new_admin)
            await message.reply_text(f"✅ User {new_admin} added as admin.")
        else:
            await message.reply_text("User is already admin.")
    except:
        await message.reply_text("Invalid user ID.")

# Remove admin command
@bot.on_message(filters.command("rev_admin") & filters.user(ADMINS))
async def remove_admin(client, message):
    parts = message.text.split(None, 1)
    if len(parts) < 2:
        await message.reply_text("Send /rev_admin <user_id>")
        return
    try:
        rem_admin = int(parts[1])
        if rem_admin in ADMINS:
            ADMINS.remove(rem_admin)
            await message.reply_text(f"✅ User {rem_admin} removed from admin list.")
        else:
            await message.reply_text("User is not an admin.")
    except:
        await message.reply_text("Invalid user ID.")

# Run bot
print("Bot is running...")
bot.run()
