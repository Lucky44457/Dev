import logging
import time

from pyrogram import Client
from pyrogram.enums import ParseMode
from telethon.sync import TelegramClient
from motor.motor_asyncio import AsyncIOMotorClient

from config import API_ID, API_HASH, BOT_TOKEN, STRING, DEFAULT_SESSION, MONGO_DB

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

botStartTime = time.time()

# MAIN BOT
app = Client(
    "pyrobot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50,
    parse_mode=ParseMode.MARKDOWN
)

# USERBOT (ONLY DEFINE)
userbot = (
    Client("userrbot", API_ID, API_HASH, session_string=DEFAULT_SESSION)
    if DEFAULT_SESSION else None
)

# TELETHON (DEFINE ONLY)
telethon_client = TelegramClient(
    "telethon_session",
    API_ID,
    API_HASH
)

# MONGO
tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]
token = tdb["tokens"]
