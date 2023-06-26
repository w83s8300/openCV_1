from PIL import ImageGrab
import numpy as np
import cv2
import time

image = ImageGrab.grab()#取的當前主螢幕
width = image.size[0]
height = image.size[1]
pTime = 0
cTime = 0
print("width:", width, "height:", height)
print("image mode:",image.mode)
 
fourcc = cv2.VideoWriter_fourcc(*'XVID')#設定編碼模式
video = cv2.VideoWriter('./test.avi', fourcc, 30, (940, 675)) # 放置的位置、編碼方式、每秒擷取幾幀、解析度
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
while True:
    img_rgb = ImageGrab.grab() #擷取大小畫面(x1,y1,x2,y2) 若要改成全螢幕ImageGrab.grab()
    img =np.array(img_rgb)
    frame = cv2.resize(img,(1600,1000))              # 縮小尺寸，避免尺寸過大導致效能不好
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   # 將鏡頭影像轉換成灰階
    faces = face_cascade.detectMultiScale(gray)      # 偵測人臉
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)   # 標記人臉
    frame=cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) #傳成opencv的BGR格式

    imgHeight = img.shape[0]
    imgWidth = img.shape[1]
    
    cTime = time.time()#現在的時間
    fps = 1/(cTime-pTime)#換算FPS
    pTime = cTime
    cv2.putText(frame, f"FPS : {int(fps)}",  (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)#把FPS畫在圖上
    cv2.imshow('oxxostudio', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()