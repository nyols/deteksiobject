import asyncio
import telegram

# Token bot Telegram Anda
TELEGRAM_TOKEN = '6080089796:AAHYeI_shzMxq7rZzVc4QgRMDg3NUM1puwA'

# ID chat Telegram yang akan menerima pemberitahuan
TELEGRAM_CHAT_ID = '1166169052'

# Fungsi untuk mengirim pesan pemberitahuan
async def kirim_pesan_pemberitahuan(pesan):
    # Membuat objek bot Telegram
    bot = telegram.Bot(token=TELEGRAM_TOKEN)

    # Mengirim pesan ke chat ID yang ditentukan
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=pesan)

# Contoh penggunaan fungsi untuk mengirim pesan pemberitahuan
pesan = "ikhwal"

asyncio.run(kirim_pesan_pemberitahuan(pesan))
