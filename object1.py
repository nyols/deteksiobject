import cv2
import telegram
import numpy as np
import asyncio

# Token bot Telegram Anda
TELEGRAM_TOKEN = '6080089796:AAHYeI_shzMxq7rZzVc4QgRMDg3NUM1puwA'

# ID chat Telegram yang akan menerima pemberitahuan
TELEGRAM_CHAT_ID = '1166169052'

# Fungsi untuk mengirim gambar ke Telegram
async def kirim_gambar_ke_telegram(gambar):
    # Membuat objek bot Telegram
    bot = telegram.Bot(token=TELEGRAM_TOKEN)

    # Mengirim gambar ke chat ID yang ditentukan
    with open('gambar.jpg', 'wb') as file:
        file.write(gambar)

    await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open('gambar.jpg', 'rb'))

async def main():
    # Inisialisasi kamera
    kamera = cv2.VideoCapture(0)

    while True:
        # Membaca frame dari kamera
        ret, frame = kamera.read()

        # Menampilkan frame di jendela gambar
        cv2.imshow('Video', frame)

        # Jika tombol 'q' ditekan, keluar dari loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Mengubah gambar ke format JPEG
        _, gambar = cv2.imencode('.jpg', frame)
        gambar = gambar.tobytes()

        # Mengirim gambar ke Telegram
        await kirim_gambar_ke_telegram(gambar)

    # Menutup kamera dan jendela tampilan gambar
    kamera.release()
    cv2.destroyAllWindows()

# Menjalankan program utama
asyncio.run(main())
