import cv2
import numpy as np
import telegram
import asyncio

# Token bot Telegram Anda
TELEGRAM_TOKEN = '6080089796:AAHYeI_shzMxq7rZzVc4QgRMDg3NUM1puwA'

# ID chat Telegram yang akan menerima pemberitahuan
TELEGRAM_CHAT_ID = '1166169052'

# Function to rescale the frame
def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

# Open the webcam
cap = cv2.VideoCapture(0)

# Function to send notification message
async def send_notification_message(message):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

while True:
    _, frame = cap.read()
    image = rescale_frame(frame, percent=100)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(gray, 150, 230)
    contours, hierarchy = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    jumlah = str(len(contours))
    print("Jumlah objek: ", jumlah)

    result_contour = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    cv2.imshow("result_contour", result_contour)
    cv2.imshow("Canny", edge)

    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == 27:  # ESC key
        break

    # Send notification message
    asyncio.run(send_notification_message("Jumlah objek: " + jumlah))

cv2.destroyAllWindows()
