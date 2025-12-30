# ---------------------------------------------------
# File Name: __init__.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/PdfsHubbb
# YouTube: https://youtube.com/@dev_gagan
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

import asyncio
import logging
import time
import importlib

from pyrogram import Client, idle
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
# Event Loop Setup (DO NOT CHANGE)
# ---------------------------------------------------

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# ---------------------------------------------------
# Logging
# ---------------------------------------------------

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

botStartTime = time.time()

# ---------------------------------------------------
# MAIN BOT (Pyrogram – BOT TOKEN)
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
# TELETHON BOT CLIENT (AS IT WAS)
# ---------------------------------------------------

telethon_client = TelegramClient(
    "telethon_session",
    API_ID,
    API_HASH
).start(bot_token=BOT_TOKEN)

# ---------------------------------------------------
# OPTIONAL PYROGRAM USER CLIENTS
# ---------------------------------------------------

# PRO CLIENT
if STRING:
    pro = Client(
        "ggbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING
    )
else:
    pro = None

# USERBOT CLIENT
if DEFAULT_SESSION:
    userrbot = Client(
        "userrbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=DEFAULT_SESSION
    )
else:
    userrbot = None

# ---------------------------------------------------
# MONGODB SETUP
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
# MAIN STARTUP FUNCTION
# ---------------------------------------------------

async def restrict_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME

    # MongoDB
    await setup_database()

    # START BOT
    await app.start()
    getme = await app.get_me()

    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    BOT_NAME = f"{getme.first_name} {getme.last_name}" if getme.last_name else getme.first_name

    print(f"Bot started as @{BOT_USERNAME}")

    # LOAD ALL MODULES (HANDLERS)
    for module in ALL_MODULES:
        importlib.import_module("devgagan.modules." + module)

    print("All modules loaded")

    # START PRO CLIENT
    if pro:
        await pro.start()
        print("Pro client started")

    # START USERBOT
    if userrbot:
        await userrbot.start()
        print("Userbot started")

# ---------------------------------------------------
# RUN BOT (KEEP ALIVE)
# ---------------------------------------------------

loop.run_until_complete(restrict_bot())
idle()
