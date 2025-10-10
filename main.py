import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# Import from config
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI, OWNER_ID, START_PIC, START_MSG, HELP_MSG

# --- INIT ---
app = Client("contact_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = AsyncIOMotorClient(MONGO_URI)
db = mongo["ContactBot"]
admins_col = db["admins"]
users_col = db["users"]

# --- UTILITIES ---
async def is_admin(user_id: int):
    admin = await admins_col.find_one({"user_id": user_id})
    return bool(admin) or user_id == OWNER_ID

async def add_user(user_id: int):
    if not await users_col.find_one({"user_id": user_id}):
        await users_col.insert_one({"user_id": user_id, "joined": datetime.utcnow()})

# --- COMMANDS ---
@app.on_message(filters.command("start"))
async def start(_, m: Message):
    await add_user(m.from_user.id)
    name = m.from_user.first_name
    caption = START_MSG.format(name=name)
    await m.reply_photo(
        START_PIC,
        caption=caption,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 Contact Admin", callback_data="contact_admin")],
            [InlineKeyboardButton("🆘 Help", callback_data="help_menu")]
        ])
    )

@app.on_callback_query(filters.regex("help_menu"))
async def help_callback(_, cq):
    await cq.message.reply_text(HELP_MSG, disable_web_page_preview=True)
    await cq.answer()

@app.on_callback_query(filters.regex("contact_admin"))
async def contact_callback(_, cq):
    await cq.message.reply_text("📝 Send me your message, and I’ll forward it to the admin.")
    await cq.answer()

@app.on_message(filters.text & ~filters.command(["start", "help", "addadmin", "deladmin", "broadcast", "admins"]))
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

@app.on_message(filters.command("help"))
async def help_cmd(_, m: Message):
    await m.reply_text(HELP_MSG, disable_web_page_preview=True)

print("🤖 Contact Bot is running...")
app.run()
