from pyrogram import Client
from ..info import logger
from ..parser import process_post_link
import asyncio
import random

reactions = {
    "positive": ["👍", "❤️", "🔥", "🌚", "👏","🎉"],
    "negative": ["🤡", "💩", "🤮", "😡", "🖕"]
}

class SendReaction:
    async def send_reaction(
        phone_number: str,
        session_string: str,
        link: str,
        emoji: str,
    ):
        link = process_post_link(link)
        app = Client(phone_number, session_string=session_string)

        if emoji in ["positive", "negative"]:
            emoji = random.choice(reactions[emoji])

        await app.connect()

        try:
            await app.send_reaction(chat_id=link["chat"],message_id=link["id"],emoji=emoji)
            await app.disconnect()
            return 1
        except Exception as e:
            logger.exception(e)
            print(emoji)
            await app.disconnect()
            return 0