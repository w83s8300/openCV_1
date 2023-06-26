
import cv2
import numpy as np

def empty(v):
    pass
# cap = cv2.VideoCapture(0)#讀相機
cap = img = cv2.imread('./kaptcha.png')


#======
cv2.namedWindow('TrackBar')
cv2.resizeWindow('TrackBar', 640, 320)

cv2.createTrackbar('Hue Min', 'TrackBar', 0, 255, empty)
cv2.createTrackbar('Hue Max', 'TrackBar', 255, 255, empty)
cv2.createTrackbar('Sat Min', 'TrackBar', 0, 255, empty)
cv2.createTrackbar('Sat Max', 'TrackBar', 255, 255, empty)
cv2.createTrackbar('Val Min', 'TrackBar', 0, 255, empty)
cv2.createTrackbar('Val Max', 'TrackBar', 255, 255, empty)
# #======

while True:
    h_min = cv2.getTrackbarPos('Hue Min', 'TrackBar')
    h_max = cv2.getTrackbarPos('Hue Max', 'TrackBar')
    s_min = cv2.getTrackbarPos('Sat Min', 'TrackBar')
    s_max = cv2.getTrackbarPos('Sat Max', 'TrackBar')
    v_min = cv2.getTrackbarPos('Val Min', 'TrackBar')
    v_max = cv2.getTrackbarPos('Val Max', 'TrackBar')
    print(h_min, h_max, s_min, s_max, v_min, v_max)
    img2gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)
    
    # ret,img = cap.read()
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)#把圖片套上hsv

    # img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

    cv2.imshow('img', img)
    cv2.imshow('hsv', hsv)
    cv2.imshow('mask', mask)
    cv2.imshow('reslut', result)
    cv2.waitKey(1)