import cv2
import mediapipe as mp
import numpy as np
import time

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands#讀取手的模型
hands = mpHands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)#
mpDraw = mp.solutions.drawing_utils#標手的座標
handLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=3)#<點的樣式(顏色,大小)
handConStyle = mpDraw.DrawingSpec(color=(255, 255, 255), thickness=5)#<線的樣式(顏色,大小)
pTime = 0
cTime = 0
Pos_8 = 0
Pos_12 = 0
x=0



#繪畫讀取的顏色
penColorBGR_B = [255, 0, 0]
penColorBGR_R = [0, 255, 0]
penColorBGR_G = [0, 0, 255]
penColorBGR_K = [0, 0, 0]

Pan_size=5#點的大小


drawPoints = []
xPos_end =999
yPos_end =999

def draw(drawpoints):#畫圖
    for point in drawpoints:
        cv2.circle(imgContour, (point[0], point[1]), Pan_size, point[2], cv2.FILLED)#找輪廓 畫點

while True:
    ret, img = cap.read()
    if ret:
        img = cv2.flip(img,1)#翻轉圖片
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)#把圖變BGR>RGB
        result = hands.process(imgRGB)#讀取圖
        # print(result.multi_hand_landmarks) #讀取手的座標
        #vvvv視窗
        imgHeight = img.shape[0]
        imgWidth = img.shape[1]

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                #mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConStyle)#檢視手的模型
                #(img<要讀的圖, handLms<把手的座標畫上去, mpHands.HAND_CONNECTIONS<把點連起來, handLmsStyle<點的樣式, handConStyle<線的樣式)
                for i, lm in enumerate(handLms.landmark):
                    xPos = int(lm.x * imgWidth)
                    yPos = int(lm.y * imgHeight)

                    # cv2.putText(img, str(i), (xPos-25, yPos+5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)#標示第幾的點
                    #            (img<要畫的圖, str(i)<標第幾的點, (xPos-25, yPos+5)<標的位子, cv2.FONT_HERSHEY_SIMPLEX<字型, 0.4<大小, (0, 0, 255)<顏色, 2<粗細)
                    if i == 8:#只要食指的點
                        cv2.circle(img, (xPos, yPos), 5, (166, 56, 56), cv2.FILLED)
                        xPos_end = xPos
                        yPos_end = yPos
                        Pos_8 = xPos + yPos
                        if cv2.waitKey(1) == ord('z'):#案z畫線 畫藍色
                            drawPoints.append([xPos, yPos, penColorBGR_B])
                        if cv2.waitKey(1) == ord('x'):#案x畫線 畫紅色
                            drawPoints.append([xPos, yPos, penColorBGR_R])
                        if cv2.waitKey(1) == ord('c'):#案c畫線 畫綠色
                            drawPoints.append([xPos, yPos, penColorBGR_G])
                    if i == 12:#只要一的點

                        cv2.circle(img, (xPos, yPos), 5, (166, 56, 56), cv2.FILLED)
                        Pos_12 = xPos + yPos

                    x=abs(int(Pos_8 - Pos_12))
                    if x < 30:
                        drawPoints.append([xPos_end, yPos_end, penColorBGR_K])

                    
                    # print(i, xPos, yPos) #標示點的座標

        imgContour = img.copy()#讀輸入相機的圖
         
        cTime = time.time()#現在的時間
        fps = 1/(cTime-pTime)#換算FPS
        pTime = cTime
        draw(drawPoints)
        cv2.putText(imgContour, "END", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)#把FPS畫在圖上
        cv2.putText(imgContour, "Re", (550, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)#把FPS畫在圖上
        cv2.putText(imgContour, f"FPS : {int(fps)}", (30, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)#把FPS畫在圖上
        cv2.imshow('imgContour', imgContour)
        print(xPos_end, yPos_end)
        if xPos_end < 100:
            if yPos_end < 50:
                break
        if xPos_end > 550:
            if yPos_end < 50:
                drawPoints = []
    if cv2.waitKey(1) == ord('q'):
        break



