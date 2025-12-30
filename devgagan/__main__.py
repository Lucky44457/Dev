# ---------------------------------------------------
# File Name: __main__.py
# ---------------------------------------------------

import asyncio
import importlib
import gc

from pyrogram import idle
from aiojobs import create_scheduler

from devgagan import app, userbot
from devgagan.modules import ALL_MODULES
from devgagan.core.mongo.plans_db import check_and_remove_expired_users

# ---------------------------------------------------
# EXPIRY CHECK
# ---------------------------------------------------

async def schedule_expiry_check():
    scheduler = await create_scheduler()
    while True:
        await scheduler.spawn(check_and_remove_expired_users())
        await asyncio.sleep(3600)
        gc.collect()

# ---------------------------------------------------
# MAIN BOOT
# ---------------------------------------------------

async def devggn_boot():

    # LOAD ALL EXISTING MODULES (NO CHANGE)
    for module in ALL_MODULES:
        importlib.import_module("devgagan.modules." + module)

    print("All modules loaded")

    # ATTACH USERBOT LOGGER (NO MODULE EDIT)
    if userbot:
        from devgagan.userbot_logger import attach_logger
        attach_logger(userbot)
        print("Userbot logger attached")

    asyncio.create_task(schedule_expiry_check())
    print("Auto removal started")

    await idle()

# ---------------------------------------------------

if __name__ == "__main__":
    asyncio.run(devggn_boot())
