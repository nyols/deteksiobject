import numpy as np
import cv2
import telegram
import asyncio

# Token bot Telegram Anda
TELEGRAM_TOKEN = '6080089796:AAHYeI_shzMxq7rZzVc4QgRMDg3NUM1puwA'

# ID chat Telegram yang akan menerima pemberitahuan
TELEGRAM_CHAT_ID = '1166169052'

classes = ["mie"]
cap = cv2.VideoCapture(0)
net = cv2.dnn.readNetFromONNX("best.onnx")

# Variable untuk menyimpan jumlah objek sebelumnya
previous_object_count = 0

# Function to send notification message
async def send_notification_message(message):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

while True:
    _, img = cap.read()

    blob = cv2.dnn.blobFromImage(img, scalefactor=1/255, size=[640, 640], mean=[0, 0, 0], swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward()[0]

    classes_ids = []
    confidences = []
    boxes = []
    rows = detections.shape[0]

    img_width, img_height = img.shape[1], img.shape[0]
    x_scale = img_width/640
    y_scale = img_height/640

    for i in range(rows):
        row = detections[i]
        confidence = row[4]
        if confidence > 0.2:
            classes_score = row[5:]
            ind = np.argmax(classes_score)
            if classes_score[ind] > 0.2:
                classes_ids.append(ind)
                confidences.append(confidence)
                cx, cy, w, h = row[:4]
                x1 = int((cx-w/2)*x_scale)
                y1 = int((cy-h/2)*y_scale)
                width = int(w * x_scale)
                height = int(h * y_scale)
                box = np.array([x1, y1, width, height])
                boxes.append(box)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.2)

    object_count = len(indices)

    if object_count != previous_object_count:
        # Send notification message
        asyncio.run(send_notification_message("Jumlah objek: " + str(object_count)))

    previous_object_count = object_count

    for i in indices:
        x1, y1, w, h = boxes[i]
        label = classes[classes_ids[i]]
        conf = confidences[i]
        text = label + "{:.2f}".format(conf)
        cv2.rectangle(img, (x1, y1), (x1+w, y1+h), (255, 0, 0), 2)
        cv2.putText(img, text, (x1, y1-2), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Deteksi Objek", img)
    if cv2.waitKey(1) & 0xff == 27:
        break

cv2.destroyAllWindows()
