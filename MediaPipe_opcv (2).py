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

#繪畫讀取的顏色
penColorBGR = [255, 0, 0]
Pan_size=5#點的大小


drawPoints = []

while True:
    ret, img = cap.read()
    if ret:
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

                    if i == 8:#只要一的點
                        cv2.circle(img, (xPos, yPos), 5, (166, 56, 56), cv2.FILLED)
                        pan = (xPos, yPos)
                        drawPoints.append([xPos, yPos, penColorBGR])
                        print([xPos, yPos, penColorBGR])
                    # print(i, xPos, yPos) #標示點的座標

        def draw(drawpoints):#畫圖
            for point in drawpoints:
                cv2.circle(imgContour, (point[0], point[1]), Pan_size, penColorBGR, cv2.FILLED)#找輪廓 畫點

        imgContour = img.copy()#讀輸入相機的圖
        cTime = time.time()#現在的時間
        fps = 1/(cTime-pTime)#換算FPS
        pTime = cTime
        draw(drawPoints)
        cv2.putText(imgContour, f"FPS : {int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)#把FPS畫在圖上
        # (imgContour, f"FPS : {int(fps)}", (30, 50)<位子, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        cv2.imshow('imgContour', imgContour)

    if cv2.waitKey(1) == ord('q'):
        break
    elif cv2.waitKey(1) == ord('w'):
        drawPoints = []