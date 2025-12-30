# ---------------------------------------------------
# File Name: __init__.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups
# ---------------------------------------------------

import asyncio
import logging
import time
import importlib

from pyrogram import Client
from pyrogram.enums import ParseMode
from telethon.sync import TelegramClient
from motor.motor_asyncio import AsyncIOMotorClient

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    STRING,
    MONGO_DB,
    DEFAULT_SESSION
)

from devgagan.modules import ALL_MODULES

# ---------------------------------------------------
# EVENT LOOP (AS ORIGINAL)
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
# MAIN BOT CLIENT
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
# TELETHON CLIENT (UNCHANGED)
# ---------------------------------------------------

telethon_client = TelegramClient(
    "telethon_session",
    API_ID,
    API_HASH
).start(bot_token=BOT_TOKEN)

# ---------------------------------------------------
# OPTIONAL CLIENTS
# ---------------------------------------------------

if STRING:
    pro = Client("ggbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING)
else:
    pro = None

if DEFAULT_SESSION:
    userrbot = Client("userrbot", api_id=API_ID, api_hash=API_HASH, session_string=DEFAULT_SESSION)
else:
    userrbot = None

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
    print("MongoDB TTL index created")

# ---------------------------------------------------
# MAIN START FUNCTION
# ---------------------------------------------------

async def restrict_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME

    await setup_database()

    # 🔥 FINAL FIX: LOAD HANDLERS FIRST
    for module in ALL_MODULES:
        importlib.import_module("devgagan.modules." + module)

    print("All modules loaded")

    # 🔥 START BOT AFTER HANDLERS
    await app.start()
    getme = await app.get_me()

    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    BOT_NAME = f"{getme.first_name} {getme.last_name}" if getme.last_name else getme.first_name

    print(f"Bot started as @{BOT_USERNAME}")

    if pro:
        await pro.start()
        print("Pro client started")

    if userrbot:
        await userrbot.start()
        print("Userbot started")

# ---------------------------------------------------
# RUN BOT (SINGLE LOOP, NO IDLE)
# ---------------------------------------------------

loop.run_until_complete(restrict_bot())
