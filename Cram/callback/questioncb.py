from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton , CallbackQuery
from Config import app , LESSONS , GROUP_ID , ADMINS , TEXT
from pyromod.exceptions.listener_timeout import ListenerTimeout
from ..data import Otherdb

@app.on_callback_query(filters.regex("#question"))
async def questioncb(client: Client, cq: CallbackQuery):
    user = cq.from_user
    classButton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("9. Sınıf", callback_data="#Class 9"),
                InlineKeyboardButton("10. Sınıf", callback_data="#Class 10"),
                InlineKeyboardButton("11. Sınıf", callback_data="#Class 11"),
            ],
            
        ]
    )

    await cq.message.edit_text(f"❔ Değerli {user.mention} hangi sınıf seviyesinde öğrencisiniz?", reply_markup=classButton)


@app.on_callback_query(filters.regex("#Class"))
async def lessoncb(client: Client, cq: CallbackQuery):
    user = cq.from_user
    StudentClass = cq.data.split()[1]
    print(LESSONS)

    if len(LESSONS) == 0:
        await cq.message.edit_text(
            f"Daha hiçbir ders eklenmedi. Lütfen daha sonra tekrar deneyin."
        )
        return

    lessonButtons = []
    row = []
    for index, lesson in enumerate(LESSONS):
        row.append(
            InlineKeyboardButton(
                lesson, callback_data=f"#Lesson  {StudentClass} {lesson}"
            )
        )
        if len(row) == 2 or index == len(LESSONS) - 1:
            lessonButtons.append(row)
            row = []

    await cq.message.edit_text(
        f"❔ Değerli {user.mention} hangi dersle ilgili sorunuz var?",
        reply_markup=InlineKeyboardMarkup(lessonButtons),
    )


@app.on_callback_query(filters.regex("#Lesson"))
async def questionchociecb(client: Client, cq: CallbackQuery):
    user = cq.from_user
    lesson = cq.data.split()[2:]
    lesson = " ".join(lesson)
    StudentClass = cq.data.split()[1]

    chociebutton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "A", callback_data=f"#Chocie {StudentClass} A {lesson}"
                ),
                InlineKeyboardButton(
                    "B", callback_data=f"#Chocie {StudentClass} B {lesson}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "C", callback_data=f"#Chocie {StudentClass} C {lesson}"
                ),
                InlineKeyboardButton(
                    "D", callback_data=f"#Chocie {StudentClass} D {lesson}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "Other", callback_data=f"#Other {StudentClass} {lesson}"
                ),
            ],
        ]
    )

    await cq.edit_message_text("➡ Lütfen bir şık seçin.", reply_markup=chociebutton)

user_sessions = {}
@app.on_callback_query(filters.regex("#Chocie"))
async def questionsendcb(client: Client, cq: CallbackQuery):
    user = cq.from_user
    chat = cq.message.chat
    StudentChoice = cq.data.split()[2]
    StudentClass = cq.data.split()[1]
    lesson = cq.data.split()[3:]
    lesson = " ".join(lesson)

    
    await cq.edit_message_text("**📤 Lütfen sorunuz fotoğrafını atın:**")
    try:
       Photo = await client.listen(chat_id=user.id ,user_id=user.id, timeout=300)
    except ListenerTimeout:
        return await cq.edit_message_text("⏳ Zaman aşımı lütfen tekrar deneyin.")
        
    if Photo.media is None:
        await cq.edit_message_text("🚫 Lütfen sadece fotoğraf atın.\nℹ Start komutu vererek sorunuzu tekrardan sorun.")
        return
    caption = f"""
#SORU

👤 **Kullanıcı:** {user.mention}
📚 **Sınıf:** {StudentClass}. Sınıf
📖 **Ders:** {lesson}
📝 **Şık:** {StudentChoice}
"""
    InfoButton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "ℹ Kullanıcı Bilgisi",
                    callback_data=f"#INF {user.id} {StudentChoice} {lesson}",
                ),
            ],
        ]
    )

    await client.send_photo(GROUP_ID, photo=Photo.photo.file_id , caption=caption , reply_markup=InfoButton)
    await cq.edit_message_text("✅ Sorunuz başarıyla gönderildi.")
    key = "sendquestion"
    value = 1
    await Otherdb.otherupdate(key , value)

@app.on_callback_query(filters.regex("#Other"))
async def questionothercb(client: Client, cq: CallbackQuery):
    user = cq.from_user
    chat = cq.message.chat
    StudentClass = cq.data.split()[1]
    lesson = cq.data.split()[2:]
    lesson = " ".join(lesson)

    await cq.edit_message_text("📤 Lütfen sorunuzu yazın:")
    try:
        text = await client.listen(chat_id=user.id, user_id=user.id, timeout=300)
    except ListenerTimeout:
        return await cq.edit_message_text("⏳ Zaman aşımı lütfen tekrar deneyin.")

    if text.text is None:
        await cq.edit_message_text("🚫 Lütfen sadece metin atın.\nℹ Start komutu vererek sorunuzu tekrardan sorun.")
        return

    await cq.message.delete()
    photo_msg = await client.send_message(chat.id, f"🖼 Şimdi lütfen sorunun resmini atın.")

    try:
        photo = await client.listen(chat_id=user.id, user_id=user.id, timeout=300)
    except ListenerTimeout:
        return await cq.edit_message_text("⏳ Zaman aşımı lütfen tekrar deneyin.")

    if photo.media is None:
        await photo_msg.edit("🚫 Lütfen sadece fotoğraf atın.\nℹ Start komutu vererek sorunuzu tekrardan sorun.")
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

    TEXT[user.id] = text.text
    await client.send_photo(
        GROUP_ID,
        photo=photo.photo.file_id,
        caption=f"""
#SORU

👤 **Kullanıcı:** {user.mention}
📚 **Sınıf:** {StudentClass}. Sınıf
📖 **Ders:** {lesson}
📝 **Soru:** {TEXT[user.id]}

""", reply_markup=InfoButton
    )
    await photo_msg.edit("✅ Sorunuz başarıyla gönderildi.")
    key = "sendquestion"
    value = 1
    await Otherdb.otherupdate(key, value)

@app.on_callback_query(filters.regex("#INF"))
async def questioncb(client: Client, cq: CallbackQuery):
    user = cq.from_user
    UserID = cq.data.split()[1]
    lesson = cq.data.split()[2]
    await cq.answer(f"👤 Kullanıcı adı: {user.username}\n🆔 Kullanıcı ID: {UserID}" , show_alert=True)


@app.on_message(filters.chat(GROUP_ID) & filters.reply)
async def replycb(client: Client, message: Message):
    user = message.from_user

    if message.reply_to_message.reply_markup is None:
        return
    elif message.reply_to_message.from_user.id != (await client.get_me()).id:
        return
    elif message.media_group_id:
        return 
    else:
        data = message.reply_to_message.reply_markup.inline_keyboard[0][0].callback_data
        user_id = data.split()[1]
        lesson = data.split()[2:]
        lesson = " ".join(lesson)
        if user.id not in ADMINS:
            return
        else:
            PointButton = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "1 ⭐", callback_data=f"#Point {user.id} 1 {lesson}"
                        ),
                        InlineKeyboardButton(
                            "2 ⭐", callback_data=f"#Point {user.id} 2 {lesson}"
                        ),
                        InlineKeyboardButton(
                            "3 ⭐", callback_data=f"#Point {user.id} 3 {lesson}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "4 ⭐", callback_data=f"#Point {user.id} 4 {lesson}"
                        ),
                        InlineKeyboardButton(
                            "5 ⭐", callback_data=f"#Point {user.id} 5 {lesson}"
                        ),
                    ],
                ]
            )
            try:
                student = await client.get_users(user_id)
            except Exception:
                await message.reply_text("**❕ Kullanıcı botu engellemiş.**")
                return

            if message.photo:
                cap = message.caption
            elif message.text:
                cap = message.text
            elif message.voice:
                cap = "`Sesli Mesaj`"
            elif message.video:
                cap = message.caption
            else:
                cap = "`Açıklama Girilmemiş`"

            if cap is None:
                cap = "`Açıklama Girilmemiş`"

            if message.reply_to_message.text:
                msg = f"🛎 Değeri {student.mention} dinlemek istedğiniz {lesson} dersi için bir mesajnız var.**\n\n📜: {cap}\n\n__Lütfen aşağıdan verilen cevabı puanlayın.__"
            else:
                msg = f"**🔔 Değerli {student.mention} {lesson} dersi için sorduğunuz soruya cevap verildi.**\n\n📜: {cap}\n\n__Lütfen aşağıdan verilen cevabı puanlayın.__"

            if message.photo:
                await client.send_photo(
                    user_id,
                    photo=message.photo.file_id,
                    caption=msg, reply_markup=PointButton
                )
            elif message.text:
                await client.send_message(
                    user_id,
                    text=msg, reply_markup=PointButton
                )
            elif  message.voice:
                await client.send_voice(
                    user_id,
                    voice=message.voice.file_id,
                    caption=msg, reply_markup=PointButton
                )
            elif message.video:
                await client.send_video(
                    user_id,
                    video=message.video.file_id,
                    caption=msg,
                    reply_markup=PointButton,
                )
            else:
                return
            if message.reply_to_message.caption:
                await message.reply_to_message.edit_text(f"📤 {message.reply_to_message.caption}\n\n__✅ {user.mention} tarafından cevap verildi.__")
            else:
                await message.reply_to_message.edit_text(f"📤 {message.reply_to_message.text}\n\n__✅ {user.mention} tarafından cevap verildi.__")

            key = "adminreply"
            value = 1
            await Otherdb.otherupdate(key , value)
@app.on_callback_query(filters.regex("#Point"))
async def questioncb(client: Client, cq: CallbackQuery):
    user = cq.from_user
    teacher_id = cq.data.split()[1]
    lesson = cq.data.split()[3:]
    lesson = " ".join(lesson)
    point = int(cq.data.split()[2])
    teacher = await client.get_users(teacher_id)
    Button = InlineKeyboardMarkup([[InlineKeyboardButton("🙏🏻 Puanınız iletildi" , callback_data="#SelectedPoint")]])
    await cq.edit_message_reply_markup(Button)
    await client.send_message(GROUP_ID, f"""
#PUAN

**ℹ Değerli {teacher.mention} {lesson} dersi için verdiğiniz yanıta puan verildi.**

- Puan veren: {user.mention} 
- UserName: @{user.username}
- Puan: {point} ⭐
""")
    
    if point >= 3:
        key =  "pozitif"
        value = 1
        await Otherdb.otherupdate(key , value)
    else:
        key = "negatif"
        value = 1
        await Otherdb.otherupdate(key , value)

@app.on_callback_query(filters.regex("#SelectedPoint"))
async def questioncb(client: Client, cq: CallbackQuery):
    await cq.answer("🎉 Görüşüzü belirttiğiniz için teşekkürler." , show_alert=True)
