import asyncio
import importlib
import gc
from pyrogram import idle

from devgagan import app, userbot
from devgagan.modules import ALL_MODULES
from devgagan.core.mongo.plans_db import check_and_remove_expired_users
from aiojobs import create_scheduler

async def schedule_expiry_check():
    scheduler = await create_scheduler()
    while True:
        await scheduler.spawn(check_and_remove_expired_users())
        await asyncio.sleep(3600)
        gc.collect()

async def main():
    # START MAIN BOT
    await app.start()
    print("Bot started")

    # START USERBOT (NEW)
    if userbot:
        await userbot.start()
        print("Userbot started")

    # LOAD ALL MODULES (restricted bot logic stays)
    for module in ALL_MODULES:
        importlib.import_module("devgagan.modules." + module)

    asyncio.create_task(schedule_expiry_check())

    await idle()   # 🔥 THIS WAS THE MISSING PIECE

    # graceful stop
    if userbot:
        await userbot.stop()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
