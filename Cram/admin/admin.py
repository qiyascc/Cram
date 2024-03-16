from pyrogram import Client, filters
from pyrogram.types import Message
from Config import app , ADMINS , DEFAULT_ADMIN
from ..data import AdminDB
from .helpers import extract_user

@app.on_message(filters.command("addadmin"))
async def add_admin(client: Client, message: Message):
    user = message.from_user

    if user.id != DEFAULT_ADMIN:
        return await message.reply("__❕ Bu komut sadece baş admin için.__")

    if not message.reply_to_message and len(message.command) < 2:
        await message.reply(
            "🔮 **Lütfen bir kullanıcıyı yanıtlayın veya bir kullanıcı kimliği girin.**"
        )
        return
    
    try:
        user_id, user_first_name = extract_user(message)
        if user_id is None:
            await message.reply("🔮 **Kullanıcı bulunamadı!**")
            return
        try:
            admin = await client.get_users(user_id)
        except Exception as e:
            await message.reply(
                "⚠️ **Kullanıcı bulunamadı, lütfen mesajını yanıtlayın veya kullanıcı adı girerek deneyin.**"
            )
            return
    except Exception as e:
        await message.reply(
            "⚠️ **Kullanıcı bulunamadı, lütfen mesajını yanıtlayın veya kullanıcı adı girerek deneyin.**"
        )
        return

    if admin.id in ADMINS:
        return await message.reply("__❕ Bu kullanıcı zaten bir admin.__")
    else:
        ADMINS.append(admin.id)
        await message.reply(f"✅ {admin.mention} __başarıyla admin olarak eklendi.__")
        await AdminDB.adminupdate()
        return


@app.on_message(filters.command("deladmin"))
async def del_admin(client: Client, message: Message):
    user = message.from_user

    if user.id != DEFAULT_ADMIN:
        return await message.reply("__❕ Bu komut sadece baş admin için.__")

    if not message.reply_to_message and len(message.command) < 2:
        await message.reply(
            "🔮 **Lütfen bir kullanıcıyı yanıtlayın veya bir kullanıcı kimliği girin.**"
        )
        return

    try:
        user_id, user_first_name = extract_user(message)
        if user_id is None:
            await message.reply("🔮 **Kullanıcı bulunamadı!**")
            return
        try:
            admin = await client.get_users(user_id)
        except Exception as e:
            await message.reply(
                "⚠️ **Kullanıcı bulunamadı, lütfen mesajını yanıtlayın veya kullanıcı adı girerek deneyin.**"
            )
            return
    except Exception as e:
        await message.reply(
            "⚠️ **Kullanıcı bulunamadı, lütfen mesajını yanıtlayın veya kullanıcı adı girerek deneyin.**"
        )
        return

    if admin.id not in ADMINS:
        return await message.reply("__❕ Bu kullanıcı zaten bir admin değil.__")
    else:
        ADMINS.remove(admin.id)
        await message.reply(f"⭕ {admin.mention} __artık admin değil.__")
        await AdminDB.adminupdate()
        return


@app.on_message(filters.command("adminlist"))
async def admin_list(client: Client, message: Message):
    user = message.from_user
    
    if user.id not in ADMINS:
        return await message.reply("__❕ Bu komut sadece adminler için.__")

    if len(ADMINS) == 0:
        return await message.reply("__❕ Hiçbir admin bulunamadı.__")

    text = "👮🏻‍♀️ **Admin Listesi:**\n\n"
    for admin in ADMINS:
        try:
            user = await client.get_users(admin)
        except Exception:
            user = None
            continue

        if admin == DEFAULT_ADMIN:
            text += f"▪ {user.mention}:(`{user.id}`)\n"
        elif user is None:
            text += f"▫ Bilinmeyen:(`{admin}`)\n"
        else:
            text += f"▫ {user.mention}:(`{user.id}`)\n"

    await message.reply(text)
    return
