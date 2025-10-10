import asyncio
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
from config import (
    API_ID, API_HASH, BOT_TOKEN, MONGO_URI, OWNER_ID,
    START_PIC, LOCAL_START_PIC, START_MSG, HELP_MSG
)

# --- INIT ---
app = Client("contact_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = AsyncIOMotorClient(MONGO_URI)
db = mongo["ContactBot"]
admins_col = db["admins"]
users_col = db["users"]
settings_col = db["settings"]

# --- UTILITIES ---
async def is_admin(user_id: int):
    admin = await admins_col.find_one({"user_id": user_id})
    return bool(admin) or user_id == OWNER_ID

async def add_user(user_id: int):
    if not await users_col.find_one({"user_id": user_id}):
        await users_col.insert_one({"user_id": user_id, "joined": datetime.utcnow()})

async def get_setting(name: str, default: str):
    data = await settings_col.find_one({"name": name})
    return data["value"] if data else default

async def set_setting(name: str, value: str):
    await settings_col.update_one({"name": name}, {"$set": {"value": value}}, upsert=True)

# --- COMMANDS ---
@app.on_message(filters.command("start"))
async def start(_, m: Message):
    await add_user(m.from_user.id)
    name = m.from_user.first_name
    caption = await get_setting("start_msg", START_MSG.format(name=name))
    image_url = await get_setting("start_pic", START_PIC)
    try:
        await m.reply_photo(
            image_url,
            caption=caption,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📩 Contact Admin", callback_data="contact_admin")],
                [InlineKeyboardButton("🆘 Help", callback_data="help_menu")]
            ])
        )
    except Exception:
        await m.reply_photo(
            LOCAL_START_PIC,
            caption=caption,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📩 Contact Admin", callback_data="contact_admin")],
                [InlineKeyboardButton("🆘 Help", callback_data="help_menu")]
            ])
        )

@app.on_callback_query(filters.regex("help_menu"))
async def help_callback(_, cq):
    help_text = await get_setting("help_msg", HELP_MSG)
    await cq.message.reply_text(help_text, disable_web_page_preview=True)
    await cq.answer()

@app.on_callback_query(filters.regex("contact_admin"))
async def contact_callback(_, cq):
    await cq.message.reply_text("📝 Send me your message, and I’ll forward it to the admin.")
    await cq.answer()

@app.on_message(filters.text & ~filters.command(
    ["start", "help", "addadmin", "deladmin", "admins", "users", "reply", "broadcast", "settings"]
))
async def handle_contact(_, m: Message):
    await add_user(m.from_user.id)
    async for admin in admins_col.find({}):
        await app.send_message(
            admin["user_id"],
            f"📬 **New Message from** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n💬 {m.text}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💭 Reply", callback_data=f"reply_{m.from_user.id}")]
            ])
        )
    await app.send_message(OWNER_ID, f"📨 Message from {m.from_user.id}: {m.text}")
    await m.reply_text("✅ Your message has been sent to the admin.")

# --- ADMIN COMMANDS ---
@app.on_message(filters.command("addadmin") & filters.user(OWNER_ID))
async def add_admin(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("Usage: /addadmin <user_id>")
    user_id = int(m.command[1])
    if await admins_col.find_one({"user_id": user_id}):
        return await m.reply_text("Already an admin.")
    await admins_col.insert_one({"user_id": user_id})
    await m.reply_text(f"✅ Added admin: `{user_id}`")

@app.on_message(filters.command("deladmin") & filters.user(OWNER_ID))
async def del_admin(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("Usage: /deladmin <user_id>")
    user_id = int(m.command[1])
    await admins_col.delete_one({"user_id": user_id})
    await m.reply_text(f"❌ Removed admin: `{user_id}`")

@app.on_message(filters.command("admins"))
async def list_admins(_, m: Message):
    if not await is_admin(m.from_user.id):
        return
    text = "👑 **Admins List:**\n\n"
    async for admin in admins_col.find({}):
        text += f"• `{admin['user_id']}`\n"
    await m.reply_text(text or "No admins found.")

@app.on_message(filters.command("users"))
async def list_users(_, m: Message):
    if not await is_admin(m.from_user.id):
        return
    count = await users_col.count_documents({})
    await m.reply_text(f"👥 **Total Users:** {count}")

@app.on_message(filters.command("reply"))
async def reply_user(_, m: Message):
    if not await is_admin(m.from_user.id):
        return
    if len(m.command) < 3:
        return await m.reply_text("Usage: /reply <user_id> <message>")
    user_id = int(m.command[1])
    msg = m.text.split(None, 2)[2]
    try:
        await app.send_message(user_id, f"💬 **Reply from Admin:**\n\n{msg}")
        await m.reply_text("✅ Reply sent successfully.")
    except Exception:
        await m.reply_text("⚠️ Failed to send message to that user.")

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("Usage: /broadcast <message>")
    msg = m.text.split(None, 1)[1]
    count = 0
    async for user in users_col.find({}):
        try:
            await app.send_message(user["user_id"], msg)
            count += 1
            await asyncio.sleep(0.1)
        except Exception:
            pass
    await m.reply_text(f"✅ Broadcast sent to {count} users.")

@app.on_message(filters.command("settings") & filters.user(OWNER_ID))
async def settings_panel(_, m: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼 Change Start Image", callback_data="set_start_pic")],
        [InlineKeyboardButton("✏️ Edit Start Message", callback_data="set_start_msg")],
        [InlineKeyboardButton("📘 Edit Help Message", callback_data="set_help_msg")]
    ])
    await m.reply_text("⚙️ **Bot Settings Panel**", reply_markup=keyboard)

@app.on_callback_query(filters.regex("^set_"))
async def set_setting_handler(_, cq):
    setting = cq.data.split("_", 1)[1]
    await cq.message.reply_text(f"📝 Send new text for **{setting.replace('msg', 'message')}** now.")
    async with app.listen(cq.message.chat.id) as response:
        msg = await response
        await set_setting(setting, msg.text)
        await cq.message.reply_text("✅ Setting updated successfully!")
    await cq.answer()

print("🤖 Contact Bot is running...")
app.run()
