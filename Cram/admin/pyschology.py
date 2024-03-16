from pyrogram import Client, filters
from pyrogram.types import Message
from Config import app, ADMINS, PYSCHOLOGY
from ..data import PyschologyDB


@app.on_message(filters.command("addproblem"))
async def add_pyschology(client: Client, message: Message):
    user = message.from_user
    if user.id not in ADMINS:
        return await message.reply("__❕ Bu komut sadece adminler için.__")
    elif len(message.command) < 2:
        await message.reply("ℹ️ Kullanım: /addproblem [Piskoloji Bölümü]")
        return
    else:
        pyschology = message.command[1:]
        pyschology = " ".join(pyschology)
        if pyschology in PYSCHOLOGY:
            return await message.reply("__❕ Bu piskoloji bölümü zaten var.__")
        else:
            PYSCHOLOGY.append(pyschology)
            await message.reply(f"✅ __{pyschology}__ __başarıyla eklendi.__")
            await PyschologyDB.pyschologyupdate()
            return

@app.on_message(filters.command("delproblem"))
async def del_pyschology(client: Client, message: Message):
    user = message.from_user
    if user.id not in ADMINS:
        return await message.reply("__❕ Bu komut sadece adminler için.__")
    elif len(message.command) < 2:
        return await message.reply("ℹ️ Kullanım: /delpysc Piskoloji Bölümü")
    else:
        pyschology = message.command[1:]
        pyschology = " ".join(pyschology)
        if pyschology not in PYSCHOLOGY:
            return await message.reply("__❕ Bu piskoloji bölümü zaten yok.__")
        else:
            await PyschologyDB.pyschologyupdate()
            PYSCHOLOGY.remove(pyschology)
            await message.reply(f"✅ __{pyschology}__ __başarıyla silindi.__")
            return
