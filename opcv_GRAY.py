import cv2
import numpy as np

kernel = np.ones((2,2),np.uint8)
kernel_1 = np.ones((2,2),np.uint8)
cap = cv2.VideoCapture(0)#讀相機

while True:
    ret, frame = cap.read()#讀輸入相機的圖
    if ret:
        frame = cv2.resize(frame, (0, 0), fx=1.2, fy=1.2)
        frame_1 = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)#變黑白
        frame_2 = cv2.GaussianBlur(frame_1,(3,3),0)#變模糊
        frame_3 = cv2.Canny(frame_2,100,150)#變2字元
        frame_4 = cv2.dilate(frame_3,kernel,iterations=1)#把2字元的線變粗
        frame_5 = cv2.erode(frame_4 ,kernel_1,iterations=1)#把2字元的線變細
        cv2.imshow('video', frame_5)

    else:
        break
    if cv2.waitKey(10) == ord('q'):
        break

