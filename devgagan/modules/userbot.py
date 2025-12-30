from pyrogram import Client
from config import API_ID, API_HASH, STRING

userbot = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING,
    in_memory=True
)
