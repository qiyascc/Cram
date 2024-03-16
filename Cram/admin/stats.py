from pyrogram import filters, Client
from pyrogram.types import Message
from Config import LESSONS, PYSCHOLOGY, USERS, BLACK_LIST, OTHERS, ADMINS, app


@app.on_message(filters.command(["stats"]))
async def stats(client, message):

    text = f"""
**ℹ Bot Bilgileri:**
 - __Toplam Kullancı:__ {len(USERS)}
 - __Toplam Yasaklı:__ {len(BLACK_LIST)}
 - __Toplam Admin:__ {len(ADMINS)}

📊 **istatistikler:**
 - __Toplam Ders:__ {len(LESSONS)}
 - __Toplam Psk. Seçeneği:__ {len(PYSCHOLOGY)}
"""
    for i in OTHERS:
        if i == "sendquestion":
            text += f" - __Toplam Sorulan Soru:__ {OTHERS['sendquestion']}\n"
        elif i == "adminreply":
            text += f" - __Toplam Verilen Cevap:__ {OTHERS['adminreply']}\n"
        elif i == "pozitif":
            text += f" - __Olumlu Bulunan Cevaplar:__ {OTHERS['pozitif']}\n"
        elif i == "negatif":
            text += f" - __Olumsuz Bulunan Cevaplar:__ {OTHERS['negatif']}\n"
        else:
            continue

    await message.reply(text)
