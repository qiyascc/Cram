from pyrogram import Client, filters
from pyrogram.types import Message
from Config import app, ADMINS , LESSONS
from ..data import LessonsDB


@app.on_message(filters.command("dellesson"))
async def del_lesson(client: Client, message: Message):
    user = message.from_user

    if user.id not in ADMINS:
        return await message.reply("__❕ Bu komut sadece adminler için.__")
    elif len(message.command) < 2:
        return await message.reply("ℹ️ Kullanım: /dellesson Ders Adı")
    else:
        lesson = message.command[1:]
        lesson = " ".join(lesson)
        if lesson not in LESSONS:
            return await message.reply("__❕ Bu ders zaten yok.__")
        else:
            await LessonsDB.lessonsupdate()
            LESSONS.remove(lesson)
            await message.reply(f"✅ __{lesson}__ __başarıyla silindi.__")
            return


@app.on_message(filters.command("addlesson"))
async def add_lesson(client: Client, message: Message):
    user = message.from_user
    print(message.text)
    if user.id not in ADMINS:
        return await message.reply("__❕ Bu komut sadece adminler için.__")
    elif len(message.command) < 2:
        await message.reply("ℹ️ Kullanım: /addlesson [Ders Adı]")
        return
    else:
        lesson = message.command[1:]
        lesson = " ".join(lesson)
        if lesson in LESSONS:
            return await message.reply("__❕ Bu ders zaten var.__")
        else:
            LESSONS.append(lesson)
            await message.reply(f"✅ __{lesson}__ __başarıyla eklendi.__")
            await LessonsDB.lessonsupdate()
            return
