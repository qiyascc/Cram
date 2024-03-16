from pyrogram import idle
from Config import app
from colorama import Fore
import asyncio
from .data import dataload

async def main():
    await dataload()
    
    try:
        await app.start()
        print(Fore.GREEN + "[BOT] Bot başlatıldı." + Fore.RESET)
    except Exception:
        print(Fore.RED + "[BOT] Bot başlatılırken bir hata oluştu." + Fore.RESET)

    await idle()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        quit(0)
