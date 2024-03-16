# ----------------------------------------------------------------------#
# Project: @NoraGuardBot - A Telegram Group Guard Bot
# Developer: <https://ContraVolta.t.me> | <https://t.me/ContraVolta>
# License: GNU V3.0 License
# GitHub: <https://github.com/krcibrahim>
# ----------------------------------------------------------------------#

import logging
from logging.handlers import RotatingFileHandler
from Config import app, ADMINS
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp

LOGGER = logging.getLogger(__name__)
LOG_FILE = "Cram.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.WARNING,
    format="%(asctime)s - Cram - %(levelname)s - %(message)s",
)

handler = RotatingFileHandler(LOG_FILE, maxBytes=1000000000000, backupCount=2)
handler.setLevel(logging.WARNING)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger("Cram")
logger.setLevel(logging.WARNING)
logger.addHandler(handler)

logger.debug("DEBUG MESSAGE!")
logger.info("INFO MESSAGE!")
logger.warning("WARN MESSAGE!")
logger.error("ERROR MESSAGE!")
logger.critical("CRITICAL MESSAGE!")


@app.on_message(filters.command("logtxt", prefixes=["/", ".", "!"]))
async def get_log(client: Client, message: Message):
    user = message.from_user
    if user.id not in ADMINS:
        return
    await message.reply_document(LOG_FILE)


@app.on_message(filters.command("log", prefixes=["/", ".", "!"]))
async def paste(client: Client, message: Message):
    user = message.from_user
    if user.id not in ADMINS:
        return
    paste_ = PASTE()
    with open(LOG_FILE, "r", encoding="iso-8859-1") as file:
        lines = file.readlines()
    log_lines = "".join(lines[-100:])

    link = await paste_.paste(log_lines)
    LinkButton = InlineKeyboardMarkup([[InlineKeyboardButton("📜 Log", url=link)]])
    await message.reply_text(f"**✅ @GizliMedyaBot Log:**", reply_markup=LinkButton)


class PASTE:
    def __init__(self):
        self.BASE = "https://batbin.me/"

    async def post(self, url: str, *args, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, *args, **kwargs) as resp:
                try:
                    data = await resp.json()
                except Exception:
                    data = await resp.text()
            return data

    async def paste(self, text: str):
        return await self.CallTone(text)

    async def CallTone(self, text):
        resp = await self.post(f"{self.BASE}api/v2/paste", data=text)
        if not resp["success"]:
            return
        link = self.BASE + resp["message"]
        return link

    async def getPaste():
        1


async def paste(text):
    a = await PASTE().paste(text)
