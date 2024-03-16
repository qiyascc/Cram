from pyrogram import Client, filters
from pyrogram.types import Message
from Config import app, BLACK_LIST, DEFAULT_ADMIN , ADMINS , GROUP_ID
from ..data import BlackDB
from .helpers import extract_user


@app.on_message(filters.command("block"))
async def block_user(client: Client, message: Message):
    user = message.from_user

    if user.id not in ADMINS:
        return await message.reply("__❕ Bu komut sadece adminler için.__")

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
            banned = await client.get_users(user_id)
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

    if banned.id in BLACK_LIST:
        return await message.reply("__❕ Bu kullanıcı zaten engellenmiş.__")
    else:
        BLACK_LIST.append(banned.id)
        await message.reply(f"✅ {banned.mention} __başarıyla engellendi.__")
        await BlackDB.blackupdate()
        await client.send_message(
            GROUP_ID,
            f"#YASAKLANDI\n\nℹ **{banned.mention}**(`{banned.id}`) **adlı kullanıcı {user.mention} tarafından yasaklandı.**",
        )
        return


@app.on_message(filters.command("unblock"))
async def unblock_user(client: Client, message: Message):
    user = message.from_user

    if user.id not in ADMINS:
        return await message.reply("__❕ Bu komut sadece adminler için.__")

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
            banned = await client.get_users(user_id)
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

    if banned.id not in BLACK_LIST:
        return await message.reply("__❕ Bu kullanıcı zaten engellenmemiş.__")
    else:
        BLACK_LIST.remove(banned.id)
        await message.reply(f"✅ {banned.mention} __başarıyla engeli kaldırıldı.__")
        await BlackDB.blackupdate()
        await client.send_message(
            GROUP_ID,
            f"#YASAK_KALDIRILDI\n\nℹ **{banned.mention} adlı kullanıcının yasağı {user.mention} tarafından kaldırıldı.**",
        )
        return


@app.on_message(filters.command("blocklist"))
async def block_list(client: Client, message: Message):
    user = message.from_user

    if user.id not in ADMINS:
        return await message.reply("__❕ Bu komut sadece adminler için.__")

    if len(BLACK_LIST) == 0:
        return await message.reply("__❕ Engellenmiş kullanıcı yok.__")

    text = "🅱 **Engellenmiş Kullanıcılar:**\n\n"
    for user_id in BLACK_LIST:
        try:
            user = await client.get_users(user_id)
        except Exception:
            user = None
            continue
        if user is None:
            text += f"• Bilinmeyen:`{user_id}`\n"
        else:
            text += f"• {user.mention}:`{user_id}`\n"

    await message.reply(text)
    return
