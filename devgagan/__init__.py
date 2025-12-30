# ---------------------------------------------------
# File Name: __init__.py
# Description: Restricted Content Saver Bot (core init)
# ---------------------------------------------------

import logging
import time

from pyrogram import Client
from pyrogram.enums import ParseMode
from telethon.sync import TelegramClient
from motor.motor_asyncio import AsyncIOMotorClient

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    STRING,
    DEFAULT_SESSION,
    MONGO_DB
)

# ---------------------------------------------------
# LOGGING
# ---------------------------------------------------

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

botStartTime = time.time()

# ---------------------------------------------------
# MAIN BOT CLIENT (BOT TOKEN)
# ---------------------------------------------------

app = Client(
    "pyrobot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode=ParseMode.MARKDOWN,
    workers=50
)

# ---------------------------------------------------
# TELETHON CLIENT (AS IT WAS)
# ---------------------------------------------------

telethon_client = TelegramClient(
    "telethon_session",
    API_ID,
    API_HASH
).start(bot_token=BOT_TOKEN)

# ---------------------------------------------------
# PRO CLIENT (STRING SESSION – OPTIONAL)
# ---------------------------------------------------

if STRING:
    pro = Client(
        "pro_client",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING
    )
else:
    pro = None

# ---------------------------------------------------
# USERBOT CLIENT (DEFAULT_SESSION – NEW)
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
# MONGODB (RESTRICTED BOT LOGIC SAFE)
# ---------------------------------------------------

tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]
token = tdb["tokens"]

async def create_ttl_index():
    await token.create_index("expires_at", expireAfterSeconds=0)

# ❌ IMPORTANT:
# YAHAN app.start(), userbot.start(), idle(), asyncio LOOP KUCH BHI NAHI
# Ye sab __main__.py handle karega
