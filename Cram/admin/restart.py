from Config import app, DEFAULT_ADMIN
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from asyncio.exceptions import CancelledError
from datetime import datetime


@app.on_message(filters.command("restart") & filters.user(DEFAULT_ADMIN))
async def resart__(client: Client, message: Message):
    await message.reply(
        f"**🔁 Bot sunucuda yeninden başlatılıyor...**",
    )

    try:
        import sys
        from os import environ, execle

        args = [sys.executable, "-m", "Cram"]

        execle(sys.executable, *args, environ)
    except CancelledError:
        print(0)
    except Exception as e:
        print(e)
