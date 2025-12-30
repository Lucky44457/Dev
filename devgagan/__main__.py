import asyncio
import importlib
import gc

from pyrogram import idle
from aiojobs import create_scheduler

from devgagan import app, userbot, telethon_client
from devgagan.modules import ALL_MODULES
from devgagan.core.mongo.plans_db import check_and_remove_expired_users

async def schedule_expiry_check():
    scheduler = await create_scheduler()
    while True:
        await scheduler.spawn(check_and_remove_expired_users())
        await asyncio.sleep(3600)
        gc.collect()

async def main():
    await app.start()
    print("Bot started")

    if userbot:
        await userbot.start()
        from devgagan.userbot_logger import attach_logger
        attach_logger(userbot)
        print("Userbot started")

    await telethon_client.start(bot_token=app.bot_token)

    for module in ALL_MODULES:
        importlib.import_module(f"devgagan.modules.{module}")

    asyncio.create_task(schedule_expiry_check())
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
