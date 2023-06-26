import cv2
import mediapipe as mp
import time
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose#讀身體的模型
mpHands = mp.solutions.hands#讀取手的模型
mpface = mp.solutions.face_mesh#讀取臉的模型

pose = mpPose.Pose()#設定身體的模型的參數
hands = mpHands.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)#設定手的模型的參數
face = mpface.FaceMesh( static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)#設定臉的模型的參數


cap = cv2.VideoCapture(0)#讀相機

LmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=3)#<點的樣式(顏色,大小)
ConStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=5)#<線的樣式(顏色,大小)

face_LmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=1)#<點的樣式(顏色,大小)
face_ConStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=1)#<線的樣式(顏色,大小)

Pan_size=5
pTime = 0
Height_x=1.5
imgWidth_y=1.5
xPos_end =999
yPos_end =999


while True:
    success, img = cap.read()
    if success:
        img = img.copy()#讀輸入相機的圖
        img = cv2.resize(img, (0, 0), fx=Height_x, fy=imgWidth_y)
        img = cv2.flip(img,1)#翻轉圖片
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)#把圖變BGR>RGB

        result_pose = pose.process(imgRGB)#讀取圖
        result_hands = hands.process(imgRGB)#讀取圖
        result_face = face.process(imgRGB)#讀取圖

        imgHeight = img.shape[0]
        imgWidth = img.shape[1]

        #放入身體的模型
        if result_pose.pose_landmarks:
            mpDraw.draw_landmarks(img, result_pose.pose_landmarks, mpPose.POSE_CONNECTIONS, LmsStyle, ConStyle)
            for id, lm in enumerate(result_pose.pose_landmarks.landmark):#檢視身體的模型
                h, w, c = img.shape
                #print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                #cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                cv2.putText(img, str(id), (cx+10, cy+10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)#標示身體第幾的點


        #放入手的模型
        if result_hands.multi_hand_landmarks:
            for handLms in result_hands.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, LmsStyle, ConStyle)#檢視手的模型
                for i, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.putText(img, str(i), (cx+10, cy+10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)#標示手第幾的點

                    if i == 8:#只要一的點
                        xPos_end = int(lm.x*100)
                        yPos_end = int(lm.y*100)

        #放入臉的模型
        #if result_face.multi_face_landmarks:
        #    for face_landmarks in result_face.multi_face_landmarks: 
        #        mpDraw.draw_landmarks( img,face_landmarks,mpface.FACEMESH_CONTOURS,face_LmsStyle,face_ConStyle)#檢視臉的模型
        #        for i, lm in enumerate(face_landmarks.landmark):
        #            h, w, c = img.shape
        #            cx, cy = int(lm.x * w), int(lm.y * h)
        #            #cv2.putText(img, str(i), (cx+10, cy+10), cv2.FONT_HERSHEY_SIMPLEX, 0.1, (0, 0, 255), 1)#標示臉第幾的點



        cTime = time.time()#現在的時間
        fps = 1/(cTime-pTime)#換算FPS
        pTime = cTime
        cv2.putText(img, "END", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)#把FPS畫在圖上
        cv2.putText(img, f"FPS : {int(fps)}", (30, imgHeight-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)#把FPS畫在圖上
        cv2.imshow('img', img)
        print(xPos_end,yPos_end)
        if xPos_end < 10:
            if yPos_end < 7:
                break

    if cv2.waitKey(1) == ord('q'):
        break
