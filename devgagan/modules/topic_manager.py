import json, asyncio
from devgagan.modules.userbot import userbot
from config import LOG_GROUP, VIP_LOG_GROUP

DB = "topics.json"
lock = asyncio.Lock()

def load():
    try:
        with open(DB) as f:
            return json.load(f)
    except:
        return {}

def save(d):
    with open(DB, "w") as f:
        json.dump(d, f, indent=2)

async def get_topic(user_id, username=None, vip=False):
    async with lock:
        data = load()
        gid = str(VIP_LOG_GROUP if vip else LOG_GROUP)

        data.setdefault(gid, {})

        if str(user_id) in data[gid]:
            return data[gid][str(user_id)]

        title = f"👤 @{username} | {user_id}" if username else f"👤 UID {user_id}"

        topic = await userbot.create_forum_topic(
            chat_id=int(gid),
            name=title
        )

        data[gid][str(user_id)] = topic.message_thread_id
        save(data)

        await asyncio.sleep(1)
        return topic.message_thread_id
