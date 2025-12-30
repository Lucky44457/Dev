from devgagan.modules.userbot import userbot
from devgagan.modules.topic_manager import get_topic
from config import LOG_GROUP, VIP_LOG_GROUP

async def send_log(user_id, username, text, vip=False):
    topic_id = await get_topic(user_id, username, vip)
    group = VIP_LOG_GROUP if vip else LOG_GROUP

    await userbot.send_message(
        chat_id=int(group),
        text=text,
        message_thread_id=topic_id
    )
