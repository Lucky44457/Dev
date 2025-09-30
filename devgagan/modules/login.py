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
import asyncio

from config import API_ID as api_id, API_HASH as api_hash

# -------------------- Helper: Delete old session silently --------------------
async def delete_old_session(user_id):
    session_file = f"session_{user_id}.session"
    try:
        if os.path.exists(session_file):
            os.remove(session_file)
    except Exception:
        pass
    await db.sessions.delete_one({"user_id": user_id})

# -------------------- Logout Command --------------------
@app.on_message(filters.command("logout"))
async def logout_user(client, message):
    user_id = message.chat.id
    await delete_old_session(user_id)
    await message.reply("✅ Logged out with flag -m")

# -------------------- Login Command with Auto-Reconnect --------------------
@app.on_message(filters.command("login"))
async def login_user(_, message):
    joined = await subscribe(_, message)
    if joined == 1:
        return

    user_id = message.chat.id

    # ---------------- Auto reconnect if session exists ----------------
    existing = await db.sessions.find_one({"user_id": user_id})
    if existing and existing.get("session_string"):
        try:
            client = TelegramClient(StringSession(existing["session_string"]), api_id, api_hash)
            await client.connect()
            # Test if session is valid
            me = await client.get_me()
            await client.disconnect()
            await message.reply(f"✅ You are already logged in as {me.first_name}. No need to login again.")
            return
        except Exception:
            # Corrupted session, proceed to normal login
            await delete_old_session(user_id)

    # ---------------- Normal login flow ----------------
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

    # Capture Telethon StringSession
    string_session = client.session.save()

    # Save/update session in MongoDB (upsert)
    await db.sessions.update_one(
        {"user_id": user_id},
        {"$set": {"session_string": string_session}},
        upsert=True
    )

    await client.disconnect()
    await otp_msg.reply("✅ Login successful! Your session has been updated.")
