from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Config import app, PYSCHOLOGY, GROUP_ID, ADMINS, TEXT


@app.on_callback_query(filters.regex("#pyschology"))
async def pyschologycb(client: Client, cq: CallbackQuery):
    user = cq.from_user

    if len(PYSCHOLOGY) == 0:
        await cq.message.edit_text(
            f"Daha hiçbir piskoloji bölümü eklenmedi. Lütfen daha sonra tekrar deneyin."
        )
        return
    # Piskoloji seçenekleri oluşturuluyor
    pyschologyButtons = []
    row = []
    for index, pyschology in enumerate(PYSCHOLOGY):
        row.append(InlineKeyboardButton(pyschology, callback_data=f"#Day {pyschology}"))
        if len(row) == 2 or index == len(PYSCHOLOGY) - 1:
            pyschologyButtons.append(row)
            row = []

    await cq.message.edit_text(
        f"**❔ Değerli {user.mention} hangi piskoloji bölümü hakında destek almak istersiniz?**",
        reply_markup=InlineKeyboardMarkup(pyschologyButtons),
    )


@app.on_callback_query(filters.regex("#Day"))
async def weekcb(client: Client, cq: CallbackQuery):
    user = cq.from_user
    pyschology = cq.data.split()[1:]
    pyschology = " ".join(pyschology)

    DayButton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Pazartesi", callback_data=f"#Time Pazartesi {pyschology}"
                ),
                InlineKeyboardButton("Salı", callback_data=f"#Time Salı {pyschology}"),
                InlineKeyboardButton(
                    "Çarşamba", callback_data=f"#Time Çarşamba {pyschology}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "Perşembe", callback_data=f"#Time Perşembe {pyschology}"
                ),
                InlineKeyboardButton("Cuma", callback_data=f"#Time Cuma {pyschology}"),
                InlineKeyboardButton(
                    "Cumartesi", callback_data=f"#Day Cumartesi {pyschology}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "Pazar", callback_data=f"#Time  Pazar {pyschology}"
                ),
            ],
        ]
    )

    await cq.message.edit_text(
        f"**❔ Değerli {user.mention} hangi gün hakkında destek almak istersiniz?**",
        reply_markup=DayButton,
    )


@app.on_callback_query(filters.regex("#Time"))
async def timecb(client: Client, cq: CallbackQuery):
    user = cq.from_user
    pyschology = cq.data.split()[2:]
    pyschology = " ".join(pyschology)
    day = cq.data.split()[1]

    TimeButton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "09:00 - 13:00",
                    callback_data=f"#SelectPysc partone {day} {pyschology}",
                ),
                InlineKeyboardButton(
                    "14:00 - 21:00",
                    callback_data=f"#SelectPysc parttwo {day} {pyschology}",
                ),
            ]
        ]
    )

    await cq.message.edit_text(
        f"**ℹ Değerli {user.mention} lütfen müsait olduğunuz saati seçin.",
        reply_markup=TimeButton,
    )


@app.on_callback_query(filters.regex("#SelectPysc"))
async def selectpysccb(client: Client, cq: CallbackQuery):
    user = cq.from_user
    pyschology = cq.data.split()[3:]
    pyschology = " ".join(pyschology)
    day = cq.data.split()[2]
    time = cq.data.split()[1]
    if time == "partone":
        timemsg = "09:00 - 13:00"
    else:
        timemsg = "14:00 - 21:00"

    AdminVerf = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ Onayla",
                    callback_data=f"#AdminVerf {day} {time} {user.id} {pyschology}",
                ),
            ]
        ]
    )
    await cq.message.edit_text(
        f"**📤 Değerli {user.mention} psikolojik destek talebiniz iletildi.**"
    )
    await client.send_message(
        GROUP_ID,
        f"""
#PSİKOLOJIK_DESTEK

🔔 **{user.mention}** adlı kullanıcı **{pyschology}** bölümü için **{day}** günü **{timemsg}** saatleri arasında psikolojik destek talebinde bulundu. 
""",
        reply_markup=AdminVerf,
    )


@app.on_callback_query(filters.regex("#AdminVerf"))
async def adminverfcb(client: Client, cq: CallbackQuery):
    user = cq.from_user

    if user.id not in ADMINS:
        return await cq.answer("❌ Bu işlemi yapmaya yetkiniz yok.", show_alert=True)

    day = cq.data.split()[1]
    time = cq.data.split()[2]
    user_id = int(cq.data.split()[3])
    pyschology = cq.data.split()[4:]
    pyschology = " ".join(pyschology)
    student = await client.get_users(user_id)
    if time == "partone":
        timemsg = "09:00 - 13:00"
    else:
        timemsg = "14:00 - 21:00"

    await cq.message.edit_text(
        f"""
**✅ Psikolojik destek talebi onaylandı.**

ℹ Ayrıntılar:
 - **Kullanıcı:** {student.mention}
 - **Piskoloji Bölümü:** {pyschology}
 - **Gün:** {day}
 - **Saat:** {timemsg}
 - **Onaylayan:** {user.mention}
"""
    )
    await client.send_message(
        user_id,
        f"""
**✅ Psikolojik destek talebiniz onaylandı.**

ℹ Ayrıntılar:
 - **Piskoloji Bölümü:** {pyschology}
 - **Gün:** {day}
 - **Saat:** {timemsg}
    """,
    )
