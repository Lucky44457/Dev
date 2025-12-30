from pyrogram import Client, filters
from config import LOG_GROUP_ID

USER_TOPICS = {}

async def get_or_create_topic(userbot: Client, user):
    uid = user.id
    if uid in USER_TOPICS:
        return USER_TOPICS[uid]

    title = f"{user.first_name or 'User'} | {uid}"
    topic = await userbot.create_forum_topic(
        chat_id=LOG_GROUP_ID,
        title=title
    )
    USER_TOPICS[uid] = topic.message_thread_id
    return topic.message_thread_id


def attach_logger(userbot: Client):

    @userbot.on_message(
        filters.private
        & filters.incoming
        & ~filters.command   # 🔥 THIS LINE SAVES YOU
    )
    async def log_private(_, msg):
        if not msg.from_user:
            return

        topic_id = await get_or_create_topic(userbot, msg.from_user)

        await userbot.send_message(
            chat_id=LOG_GROUP_ID,
            message_thread_id=topic_id,
            text=(
                f"👤 User: {msg.from_user.mention}\n"
                f"🆔 ID: `{msg.from_user.id}`\n"
                f"💬 Text: {msg.text or 'Media'}"
            )
    )
