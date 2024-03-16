from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
)
from pyromod.exceptions.listener_timeout import ListenerTimeout
from Config import (
    app,
    ADMINS,
    LESSONS,
    PYSCHOLOGY,
    GROUP_ID,
    DEFAULT_ADMIN,
    USERS,
    BLACK_LIST,
    SUPPORT,
)
from .data import LessonsDB, PyschologyDB, AdminDB, UserDB, BlackDB


@app.on_message(filters.command(["start"]) & filters.private)
async def start(client: Client, message: Message):
    user = message.from_user
    if user.id not in USERS:
        USERS.append(user.id)
        await client.send_message(
            GROUP_ID,
            f"#YENI_KULLANICI\n\n**ℹ Ayrıntılar:**\n - __Kullanıcı:__ {user.mention}\n - __Kullanıcı ID:__ `{user.id}`\n - __Kullanıcı Username:__ @{user.username}",
        )
        await UserDB.userupdate()

    if user.id in BLACK_LIST:
        SupButton = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⛑ Destek Ekibi", url=f"https://t.me/{SUPPORT}"
                    ),
                ],
            ]
        )
        return await message.reply_text(
            "**⭕ Bir yönetici tarafından yasaklandığın için botu kullanamazsın.**\n\nℹ __Eğer bunun bir hata olduğunu düşünüyorsa destek ekbine yazabilirsin.__",
            reply_markup=SupButton,
        )

    if user.id in ADMINS:
        AdminButton = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔒 Yönetici Paneli", callback_data="#adminpanel"
                    ),
                ],
            ]
        )

        await message.reply_text(
            f"👋🏻 Merhaba {user.mention}(ADMIN) sana nasıl yardımcı olabilirim.",
            reply_markup=AdminButton,
        )
    else:
        StartButton = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("❔ Sorum Var", callback_data="#question"),
                    InlineKeyboardButton(
                        "👂🏻 Dinlemek İstiyorum", callback_data="#listenlesson"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "⛑ Psikolojik Destek", callback_data="#pyschology"
                    ),
                ],
            ]
        )

        await message.reply_text(
            f"""
👋🏻 Merhaba {user.mention} sana nasıl yardımıcı olabilirim.
""",
            reply_markup=StartButton,
        )


@app.on_callback_query(filters.regex("#backpanel"))
async def backmenu(client: Client, cq: CallbackQuery):

    Buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📚 Ders Ekle", callback_data="#paneladdlesson"),
                InlineKeyboardButton("🆑 Ders Sil", callback_data="#paneldellesson"),
            ],
            [
                InlineKeyboardButton(
                    "💬 Psk. Destek Ekle", callback_data="#paneladdpyschology"
                ),
                InlineKeyboardButton(
                    "🆑 Psk. Destek Sil", callback_data="#paneldelpyschology"
                ),
            ],
            [
                InlineKeyboardButton(
                    "👮🏻‍♂️ Admin Ekle - Sil", callback_data="#paneladdadmin"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🅱 Kullanıcı Yasakla - Kaldır", callback_data="#panelblacklist"
                ),
                InlineKeyboardButton("📚 Komutlar", callback_data="#commandsadmin"),
            ],
        ]
    )

    await cq.edit_message_text("**ℹ Lütfen bir işlem seçiniz.**", reply_markup=Buttons)


@app.on_callback_query(filters.regex("#adminpanel"))
async def adminpanels(client: Client, cq: CallbackQuery):

    Buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📚 Ders Ekle", callback_data="#paneladdlesson"),
                InlineKeyboardButton("🆑 Ders Sil", callback_data="#paneldellesson"),
            ],
            [
                InlineKeyboardButton(
                    "💬 Psk. Destek Ekle", callback_data="#paneladdpyschology"
                ),
                InlineKeyboardButton(
                    "🆑 Psk. Destek Sil", callback_data="#paneldelpyschology"
                ),
            ],
            [
                InlineKeyboardButton(
                    "👮🏻‍♂️ Admin Ekle - Sil", callback_data="#paneladdadmin"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🅱 Kullanıcı Yasakla - Kaldır", callback_data="#panelblacklist"
                ),
                InlineKeyboardButton("📚 Komutlar", callback_data="#commandsadmin"),
            ],
        ]
    )

    await cq.edit_message_text("**ℹ Lütfen bir işlem seçiniz.**", reply_markup=Buttons)


@app.on_callback_query(filters.regex("#paneladdlesson"))
async def PanelAddLesson(client: Client, cq: CallbackQuery):
    user = cq.from_user
    chat = cq.message.chat

    await cq.edit_message_text("**➡ Lütfen eklemek istediğiniz dersi yazınız:**")
    try:
        lesson = await client.listen(chat_id=chat.id, user_id=user.id, timeout=300)
    except ListenerTimeout:
        return await cq.edit_message_text("__⏳ Zaman aşımı lütfen tekrar deneyin.__")

    if lesson.text:
        LESSONS.append(lesson.text)
        await LessonsDB.lessonsupdate()
        await cq.edit_message_text(f"**✅ {lesson.text} dersi başarıyla eklendi.**")
        await client.send_message(
            GROUP_ID,
            f"""
#DERS_EKLENDI

**ℹ Ayrıntılar:**
 - __Ders:__ {lesson.text}
 - __Ekleyen:__ {user.mention}
 - __Ekleyen ID:__ `{user.id}`
    """,
        )
    else:
        await cq.edit_message_text("**⭕ Lütfen sadece metin giriniz.**")


@app.on_callback_query(filters.regex("#paneladdpyschology"))
async def PanelAddPyschology(client: Client, cq: CallbackQuery):
    user = cq.from_user
    chat = cq.message.chat

    await cq.edit_message_text(
        "**➡ Lütfen eklemek istediğiniz psikolojik destek metnini yazınız:**"
    )

    try:
        lesson = await client.listen(chat_id=chat.id, user_id=user.id, timeout=300)
    except ListenerTimeout:
        return await cq.edit_message_text("__⏳ Zaman aşımı lütfen tekrar deneyin.__")

    if lesson.text:
        PYSCHOLOGY.append(lesson.text)
        await PyschologyDB.pyschologyupdate()
        await cq.edit_message_text(f"**✅ Psikolojik destek metni başarıyla eklendi.**")
        await client.send_message(
            GROUP_ID,
            f"""
#PSIKOLJI_METNI_EKLENDI

**ℹ Ayrıntılar:**
 - __Metin:__ {lesson.text}
 - __Ekleyen:__ {user.mention}
 - __Ekleyen ID:__ `{user.id}`

""",
        )
    else:
        await cq.edit_message_text("**⭕ Lütfen sadece metin giriniz.**")


@app.on_callback_query(filters.regex("#paneldellesson"))
async def PanelDelLesson(client: Client, cq: CallbackQuery):

    if len(LESSONS) == 0:
        return await cq.edit_message_text("**⭕ Hiç ders bulunmamaktadır.**")

    LesButton = []
    row = []

    lessonButtons = []
    row = []
    for index, lesson in enumerate(LESSONS):
        row.append(InlineKeyboardButton(lesson, callback_data=f"#DeleteLeson {lesson}"))
        if len(row) == 2 or index == len(LESSONS) - 1:
            lessonButtons.append(row)
            row = []
    lessonButtons.append([InlineKeyboardButton("◀ Geri", callback_data="#backpanel")])

    await cq.edit_message_text(
        f"**🗑 Silmek istediğiniz dersi seçiniz.**",
        reply_markup=InlineKeyboardMarkup(lessonButtons),
    )


@app.on_callback_query(filters.regex("#paneldelpyschology"))
async def PanelDellPpyschology(client: Client, cq: CallbackQuery):

    if len(PYSCHOLOGY) == 0:
        return await cq.edit_message_text(
            "**⭕ Hiç psikolojik destek metni bulunmamaktadır.**"
        )

    LesButton = []
    row = []

    lessonButtons = []
    row = []
    for index, lesson in enumerate(PYSCHOLOGY):
        row.append(
            InlineKeyboardButton(lesson, callback_data=f"#DeletePyschology {lesson}")
        )
        if len(row) == 2 or index == len(PYSCHOLOGY) - 1:
            lessonButtons.append(row)
            row = []
    lessonButtons.append([InlineKeyboardButton("◀ Geri", callback_data="#backpanel")])

    await cq.edit_message_text(
        f"**🗑 Silmek istediğiniz psikolojik destek metnini seçiniz.**",
        reply_markup=InlineKeyboardMarkup(lessonButtons),
    )


@app.on_callback_query(filters.regex("#DeleteLeson"))
async def delete_lesson(client: Client, cq: CallbackQuery):

    lesson = cq.data.split()[1:]
    lesson = " ".join(lesson)

    if lesson in LESSONS:
        LESSONS.remove(lesson)
        await LessonsDB.lessonsupdate()
        await cq.edit_message_text(
            f"**✅ {lesson} dersi başarıyla silindi.**",
            reply_markup=InlineKeyboardMarkup(
                [InlineKeyboardButton("◀ Geri", callback_data="#backpanel")]
            ),
        )
        await client.send_message(
            GROUP_ID,
            f"""
#DERS_SILINDI

**ℹ Ayrıntılar:**
 - __Silinen Ders:__ {lesson}
 - __Kullanıcı:__ {cq.from_user.mention}
 - __Kullanıcı Id:__ `{cq.from_user.id}`
    """,
        )
    else:
        await cq.edit_message_text(
            "**⭕ Böyle bir ders bulunmamaktadır.**",
            reply_markup=InlineKeyboardMarkup(
                [InlineKeyboardButton("◀ Geri", callback_data="#backpanel")]
            ),
        )


@app.on_callback_query(filters.regex("#DeletePyschology"))
async def delete_pyschology(client: Client, cq: CallbackQuery):

    lesson = cq.data.split()[1:]
    lesson = " ".join(lesson)

    BackButton = InlineKeyboardMarkup(
        [InlineKeyboardButton("◀ Geri", callback_data="#backpanel")]
    )

    if lesson in PYSCHOLOGY:
        PYSCHOLOGY.remove(lesson)
        await PyschologyDB.pyschologyupdate()
        await cq.edit_message_text(
            f"**✅ Psikolojik destek metni başarıyla silindi.**",
            reply_markup=BackButton,
        )
        await client.send_message(
            GROUP_ID,
            f"""
#PSIKOLOJIK_METNI_SILINDI

**ℹ Ayrıntılar:**
 - __Silinen Metin:__ {lesson}
 - __Kullanıcı:__ {cq.from_user.mention}
 - __Kullanıcı Id:__ `{cq.from_user.id}`
    """,
        )
    else:
        await cq.edit_message_text(
            "**⭕ Böyle bir psikolojik destek metni bulunmamaktadır.**",
            reply_markup=BackButton,
        )


@app.on_callback_query(filters.regex("#paneladdadmin"))
async def PanelAddAdmin(client: Client, cq: CallbackQuery):

    user = cq.from_user
    chat = cq.message.chat

    if user.id != DEFAULT_ADMIN:
        return await cq.answer(
            "❕ Bu işlemi sadece baş admin yapabilir.", show_alert=True
        )

    await cq.edit_message_text(
        "**👮🏻‍♂️ Lütfen eklemek veya silmek istediğiniz kullanıcnın ID'sini veya Kullanıcı adını atınız:**"
    )

    try:
        text = await client.listen(chat_id=chat.id, user_id=user.id, timeout=300)
    except ListenerTimeout:
        return await cq.edit_message_text("__⏳ Zaman aşımı lütfen tekrar deneyin.__")

    try:
        admin = await client.get_users(text.text)
    except Exception:
        return await cq.edit_message_text(
            "**⭕ Kullanıcı bulunamadı lütfen botu başlatmasını isteyin.**"
        )

    if admin.id in ADMINS:
        ADMINS.remove(admin.id)
        await AdminDB.adminupdate()
        await cq.edit_message_text(
            f"**⭕ {admin.mention} başarıyla adminlikten silindi.**"
        )
        await client.send_message(
            GROUP_ID,
            f"""
#ADMIN_SILINDI

**ℹ Ayrıntılar:**
 - __Admin:__ {admin.mention}
 - __Admin ID:__ `{admin.id}`
 - __Admin Username:__ @{admin.username}
    
    """,
        )
    else:
        ADMINS.append(admin.id)
        await AdminDB.adminupdate()
        await cq.edit_message_text(f"**✅ {admin.mention} başarıyla admin yapıldı.**")
        await client.send_message(
            GROUP_ID,
            f"""
#YENI_ADMIN

**ℹ Ayrıntılar:**
 - __Admin:__ {admin.mention}
 - __Admin ID:__ `{admin.id}`
 - __Admin Username:__ @{admin.username}
    """,
        )
        return


@app.on_callback_query(filters.regex("#panelblacklist"))
async def PanelBlackList(client: Client, cq: CallbackQuery):

    user = cq.from_user
    chat = cq.message.chat

    await cq.edit_message_text(
        "**👮🏻‍♂️ Lütfen yasaklamak veya yasağı kaldırmak istediğiniz kullanıcnın ID'sini veya Kullanıcı adını atınız:**"
    )

    try:
        text = await client.listen(chat_id=chat.id, user_id=user.id, timeout=300)
    except ListenerTimeout:
        return await cq.edit_message_text("__⏳ Zaman aşımı lütfen tekrar deneyin.__")

    try:
        banned = await client.get_users(text.text)
    except Exception:
        return await cq.edit_message_text(
            "**⭕ Kullanıcı bulunamadı lütfen botu başlatmasını isteyin.**"
        )

    if banned.id in BLACK_LIST:
        BLACK_LIST.remove(banned.id)
        await BlackDB.blackupdate()
        await cq.edit_message_text(
            f"**✅ {banned.mention} başarıyla yasak kaldırıldı.**"
        )
        await client.send_message(
            GROUP_ID,
            f"#YASAK_KALDIRILDI\n\nℹ **{banned.mention} adlı kullanıcının yasağı {user.mention} tarafından kaldırıldı.**",
        )
    else:
        BLACK_LIST.append(banned.id)
        await BlackDB.blackupdate()
        await cq.edit_message_text(f"**✅ {banned.mention} başarıyla yasaklandı.**")
        await client.send_message(
            GROUP_ID,
            f"#YASAKLANDI\n\nℹ **{banned.mention}**(`{banned.id}`) **adlı kullanıcı {user.mention} tarafından yasaklandı.**",
        )
        return


@app.on_callback_query(filters.regex("#commandsadmin"))
async def CommandPanel(client: Client, cq: CallbackQuery):

    Button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("◀ Geri", callback_data="#backpanel")]]
    )

    await cq.edit_message_text(
        """
ℹ Admin Komutları:
 ▫ /addlesson [Ders Adı] - Ders ekler.
 
 ▫ /dellesson [Ders ADI] - Ders siler.
 
 ▫ /addproblem [Mesaj] - Psikoloji seçeneği ekler.
 
 ▫ /delproblem [Mesaj] - Psikoloji seçeneği siler.
 
 ▫ /stats - Bot hakkında bilgi verir.
 
 ▫ /block [ID , Reply or Username] - Kullanıcıyı engeller.
 
 ▫ /ublock [ID , Reply or Username] - Kullanıcı engelini kaldırır.
 
 ▫ /broadcast [Reply] - Yayin mesajı gönderir.
 
 ▫ /restart - Botu sunucuda yeniden başlatır.
""",
        reply_markup=Button,
    )
