
import cv2

img = cv2.imread('000.jpeg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faceCascade = cv2.CascadeClassifier('face_detect.xml')#套用模型  到https://github.com/opencv/opencv/tree/4.x/data/haarcascades找你要的模型
faceRect = faceCascade.detectMultiScale(gray, 1.1, 6)
print(len(faceRect))

for (x, y, w, h) in faceRect:#畫出模型找到的
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    print (x,y,w,h)
cv2.imshow('img', img)
cv2.waitKey(0)