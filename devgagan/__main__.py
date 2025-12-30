import asyncio
import importlib
import gc

from pyrogram import idle
from aiojobs import create_scheduler

from devgagan import app, userbot
from devgagan.modules import ALL_MODULES
from devgagan.core.mongo.plans_db import check_and_remove_expired_users


# ---------------- EXPIRY SCHEDULER ---------------- #

async def schedule_expiry_check():
    scheduler = await create_scheduler()
    while True:
        await scheduler.spawn(check_and_remove_expired_users())
        await asyncio.sleep(3600)  # 1 hour
        gc.collect()


# ---------------- MAIN ENTRY ---------------- #

async def main():

    # 1️⃣ LOAD ALL MODULES FIRST (IMPORTANT)
    for module in ALL_MODULES:
        importlib.import_module("devgagan.modules." + module)

    print("All modules loaded")

    # 2️⃣ START MAIN BOT AFTER HANDLERS ARE REGISTERED
    await app.start()
    print("Bot started")

    # 3️⃣ START USERBOT (OPTIONAL)
    if userbot:
        await userbot.start()
        print("Userbot started")

    # 4️⃣ START BACKGROUND TASKS
    asyncio.create_task(schedule_expiry_check())
    print("Expiry scheduler started")

    # 5️⃣ KEEP BOT ALIVE
    await idle()

    # 6️⃣ GRACEFUL SHUTDOWN
    if userbot:
        await userbot.stop()
    await app.stop()


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    asyncio.run(main())
