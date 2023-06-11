import cv2
import numpy as np
import telegram
from telegram import InputFile

# Inisialisasi klien Telegram Bot
bot_token = '6080089796:AAHYeI_shzMxq7rZzVc4QgRMDg3NUM1puwA'
bot = telegram.Bot(token=bot_token)

#!rescale saja default 75 persen dari 640x320
def rescale_frame(frame,percent=75):
    width=int(frame.shape[1]* percent/100)
    height=int(frame.shape[0]* percent/100)
    dim = (width,height)
    return cv2.resize(frame,dim,interpolation=cv2.INTER_AREA)
##! port webcam di sesuaikan 0 untuk internal dan lainnya untuk external
cap = cv2.VideoCapture(0)
while(True):
    _, frame = cap.read()
    image = rescale_frame(frame,percent=100)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(gray,150,200)
    contours , hierarchy = cv2.findContours(edge,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    jumlah = str(len(contours))

    chat_id = '1166169052'
    bot.send_photo(chat_id=chat_id, photo=telegram.InputFile("jumlah objek : ",jumlah))

    result_contour = cv2.drawContours(image,contours,-1,(0,255,0),2)
    cv2.imshow("result_contour",result_contour)  
    #cv2.imshow("kamera",image)
    cv2.imshow("Canny",edge)
    
    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == 27: #esc key
        break
cv2.waitkey(0)
cv2.destroyAllWindows()