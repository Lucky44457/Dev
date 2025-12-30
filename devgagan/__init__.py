# ---------------------------------------------------
# File Name: __init__.py
# ---------------------------------------------------

import asyncio
import logging
import time

from pyrogram import Client
from pyrogram.enums import ParseMode
from telethon.sync import TelegramClient
from motor.motor_asyncio import AsyncIOMotorClient

from config import API_ID, API_HASH, BOT_TOKEN, STRING, DEFAULT_SESSION, MONGO_DB

# ---------------------------------------------------
# EVENT LOOP (AS YOU HAD)
# ---------------------------------------------------

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# ---------------------------------------------------
# LOGGING
# ---------------------------------------------------

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

botStartTime = time.time()

# ---------------------------------------------------
# MAIN BOT
# ---------------------------------------------------

app = Client(
    "pyrobot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50,
    parse_mode=ParseMode.MARKDOWN
)

# ---------------------------------------------------
# TELETHON (AS IT WAS)
# ---------------------------------------------------

telethon_client = TelegramClient(
    "telethon_session",
    API_ID,
    API_HASH
)

# ---------------------------------------------------
# PRO CLIENT
# ---------------------------------------------------

if STRING:
    pro = Client(
        "ggbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING
    )
else:
    pro = None

# ---------------------------------------------------
# USERBOT (ONLY FOR LOG TOPICS)
# ---------------------------------------------------

if DEFAULT_SESSION:
    userbot = Client(
        "userrbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=DEFAULT_SESSION
    )
else:
    userbot = None

# ---------------------------------------------------
# MONGODB
# ---------------------------------------------------

tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]
token = tdb["tokens"]

async def create_ttl_index():
    await token.create_index("expires_at", expireAfterSeconds=0)

async def setup_database():
    await create_ttl_index()
    print("MongoDB TTL index created.")

# ---------------------------------------------------
# STARTUP FUNCTION (OLD LOGIC SAFE)
# ---------------------------------------------------

async def restrict_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME

    await setup_database()

    await app.start()
    getme = await app.get_me()

    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    BOT_NAME = f"{getme.first_name} {getme.last_name}" if getme.last_name else getme.first_name

    if pro:
        await pro.start()

    if userbot:
        await userbot.start()

    await telethon_client.start(bot_token=BOT_TOKEN)

loop.run_until_complete(restrict_bot())
