from pyrogram import Client, filters
from Config import app, USERS, DEFAULT_ADMIN
from pyrogram.errors import FloodWait
from pyrogram.types import Message
import asyncio


@app.on_message(filters.command("broadcast"))
async def broadcast(client: Client, message: Message):
    user = message.from_user
    if user.id != DEFAULT_ADMIN:
        return await message.reply("❕ **Bu komut sadece baş admin için.**")

    if not message.reply_to_message:
        return await message.reply_text("❕ **Lütfen bir mesaj yanıtlayın.**")
    else:
        message_to_broadcast = message.reply_to_message
        for user in USERS:
            try:
                await message_to_broadcast.forward(chat_id=user)
                await asyncio.sleep(3)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as e:
                pass
