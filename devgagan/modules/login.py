from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    SessionPasswordNeededError, PhoneCodeInvalidError,
    PhoneCodeExpiredError
)
from pyrogram import filters
from devgagan import app
from devgagan.core.mongo import db
from devgagan.core.func import subscribe
import os

from config import API_ID as api_id, API_HASH as api_hash

async def delete_old_session(user_id):
    session_file = f"session_{user_id}.session"
    # Delete old session file if exists
    if os.path.exists(session_file):
        os.remove(session_file)
    # Delete old session string from DB
    await db.sessions.delete_one({"user_id": user_id})

@app.on_message(filters.command("logout"))
async def logout_user(client, message):
    user_id = message.chat.id
    await delete_old_session(user_id)
    await message.reply("✅ Logout Successfull!")

@app.on_message(filters.command("login"))
async def login_user(_, message):
    joined = await subscribe(_, message)
    if joined == 1:
        return

    user_id = message.chat.id

    # Auto delete old session before new login
    await delete_old_session(user_id)

    number_msg = await _.ask(user_id, "Enter your phone number with country code:\nExample: +19876543210", filters=filters.text)
    phone_number = number_msg.text

    client = TelegramClient(StringSession(), api_id, api_hash)
    await client.connect()

    try:
        sent_code = await client.send_code_request(phone_number)
    except Exception as e:
        await message.reply(f"❌ Failed to send code: {e}")
        await client.disconnect()
        return

    try:
        otp_msg = await _.ask(user_id, "Enter the OTP sent to your Telegram account:", filters=filters.text, timeout=600)
        otp_code = otp_msg.text.replace(" ", "")
    except TimeoutError:
        await message.reply("⏰ OTP timeout. Please restart login.")
        await client.disconnect()
        return

    try:
        await client.sign_in(phone_number, code=otp_code, phone_code_hash=sent_code.phone_code_hash)
    except PhoneCodeInvalidError:
        await otp_msg.reply("❌ Invalid OTP. Restart login.")
        await client.disconnect()
        return
    except PhoneCodeExpiredError:
        await otp_msg.reply("❌ OTP expired. Restart login.")
        await client.disconnect()
        return
    except SessionPasswordNeededError:
        try:
            pwd_msg = await _.ask(user_id, "Two-step verification enabled. Enter your password:", filters=filters.text, timeout=300)
            await client.sign_in(password=pwd_msg.text)
        except TimeoutError:
            await message.reply("⏰ Password timeout. Restart login.")
            await client.disconnect()
            return

    # Capture Telethon string session
    string_session = client.session.save()

    # Save new session string in MongoDB (upsert)
    await db.sessions.update_one(
        {"user_id": user_id},
        {"$set": {"session_string": string_session}},
        upsert=True
    )

    await client.disconnect()
    await otp_msg.reply("✅ Login successful!")
