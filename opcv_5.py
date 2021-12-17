import cv2
import numpy as np


cap = cv2.VideoCapture(0)#讀相機
Pan_size=5

# Blue Green Yellowq 判斷顏色
penColorHSV = [[107, 134, 118, 113, 224, 255],
               [0, 112, 134, 10, 144, 255],
               [33, 60, 134, 52, 144, 255]]
#繪畫讀取的顏色
penColorBGR = [[255, 0, 0],
               [0, 255, 0],
               [0, 0, 255]]

# [x, y, colorId]
drawPoints = []


def findPen(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    for i in range(len(penColorHSV)):#跑顏色
        lower = np.array(penColorHSV[i][:3])
        upper = np.array(penColorHSV[i][3::])

        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(img, img, mask=mask)#把圖片套上hsv
        penx, peny = findContour(mask)
        cv2.circle(imgContour, (penx, peny), Pan_size, penColorBGR[i], cv2.FILLED)#找輪廓 畫點
        if peny!=-1:
            drawPoints.append([penx, peny, i])#留下顏色
    # cv2.imshow('result', result)

def findContour(img):#讀取筆尖
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)#找輪廓 用.CHAIN_APPROX_NONE的方法
    x, y, w, h = -1, -1, -1, -1
    for cnt in contours:
        # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 4)#畫輪廓
        area = cv2.contourArea(cnt)#輪廓面積
        if area > 500:
            peri = cv2.arcLength(cnt, True)#輪廓種長
            vertices = cv2.approxPolyDP(cnt, peri * 0.02, True)#近似多邊形
            x, y, w, h = cv2.boundingRect(vertices)#輪廓總長  

    return x+w//2, y


def draw(drawpoints):#畫圖
    for point in drawpoints:
        cv2.circle(imgContour, (point[0], point[1]), Pan_size, penColorBGR[point[2]], cv2.FILLED)#找輪廓 畫點

while True:
    ret, frame = cap.read()
    if ret:
        imgContour = frame.copy()#讀輸入相機的圖
        # cv2.imshow('video', frame)
        findPen(frame)
        draw(drawPoints)
        cv2.imshow('contour', imgContour)
    else:
        break
    if cv2.waitKey(1) == ord('q'):
        break
    elif cv2.waitKey(1) == ord('w'):
        drawPoints = []
