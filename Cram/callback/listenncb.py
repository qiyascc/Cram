from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Config import app, LESSONS, GROUP_ID, ADMINS, TEXT
from pyromod.exceptions.listener_timeout import ListenerTimeout

@app.on_callback_query(filters.regex("#listenlesson"))
async def listencb(client: Client, cq: CallbackQuery):
    user = cq.from_user
    classButton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("9. Sınıf", callback_data="#SelectLesson 9"),
                InlineKeyboardButton("10. Sınıf", callback_data="#SelectLesson 10"),
                InlineKeyboardButton("11. Sınıf", callback_data="#SelectLesson 11"),
            ],
        ]
    )

    await cq.message.edit_text(
        f"❔ Değerli {user.mention} hangi sınıf seviyesinde öğrencisiniz?",
        reply_markup=classButton,
    )


@app.on_callback_query(filters.regex("#SelectLesson"))
async def listenlessonselected(client: Client, cq: CallbackQuery):
    user = cq.from_user
    StudentClass = cq.data.split()[1]
    print(LESSONS)

    if len(LESSONS) == 0:
        await cq.message.edit_text(
            f"😥 **Daha hiçbir ders eklenmedi. Lütfen daha sonra tekrar deneyin.**"
        )
        return

    lessonButtons = []
    row = []
    for index, lesson in enumerate(LESSONS):
        row.append(
            InlineKeyboardButton(
                lesson, callback_data=f"#ListenSelected {StudentClass} {lesson}"
            )
        )
        if len(row) == 2 or index == len(LESSONS) - 1:
            lessonButtons.append(row)
            row = []

    await cq.message.edit_text(
        f"❔ Değerli {user.mention} hangi dersle ilgili yardım almak istersiniz.",
        reply_markup=InlineKeyboardMarkup(lessonButtons),
    )


@app.on_callback_query(filters.regex("#ListenSelected"))
async def listencbselected(client: Client, cq: CallbackQuery):
    user = cq.from_user
    chat = cq.message.chat
    StudentClass = cq.data.split()[1]
    lesson = cq.data.split()[2:]
    lesson = " ".join(lesson)

    await cq.message.edit_text(
        f"**✍🏻 {lesson} dersi için bilgi sahibi olmak istediğiniz konuyu yazınız:**"
    )
    try:
        konu = await client.listen(chat_id=user.id ,user_id=user.id, timeout=300)
    except ListenerTimeout:
        return await cq.edit_message_text("__⏳ Zaman aşımı lütfen tekrar deneyin.__")

    if not konu.text:
        await cq.edit_message_text("❗")
        return

    InfoButton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "ℹ Kullanıcı Bilgisi",
                    callback_data=f"#INF {user.id} {lesson}",
                ),
            ],
        ]
    )

    await cq.edit_message_text(
        f"📚 {lesson} dersi için {konu.text} konusunda yardım alma talebinizi aldık."
    )
    await client.send_message(
        GROUP_ID,
        f"""
#DINLEME

👤 **{user.mention}** adlı kullanıcı **{lesson}** dersi için **{konu.text}** konusunda ders dinlemek istiyor.
""",
        reply_markup=InfoButton,
    )
