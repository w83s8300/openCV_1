import cv2

img = cv2.imread('shape.jpg')
imgContour = img.copy()
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#變黑白
canny = cv2.Canny(img, 150, 200)
contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)#找輪廓 用.CHAIN_APPROX_NONE的方法

for cnt in contours:
    cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 4)#畫輪廓
    area = cv2.contourArea(cnt)#輪廓面積
    
    if area > 500:
        # print(cv2.arcLength(cnt, True))#輪廓種長
        peri = cv2.arcLength(cnt, True)
        vertices = cv2.approxPolyDP(cnt, peri * 0.02, True)#近似多邊形
        corners = len(vertices)#判斷圖的角
        x, y, w, h = cv2.boundingRect(vertices)#輪廓總長
        cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 255, 0), 4)#標示出範圍
        if corners == 3:
            cv2.putText(imgContour, 'triangle', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    #(imgContour要讀的圖, 'triangle'要寫的字, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX字型, 1字的大小, (0, 0, 255)字的顏色, 2線的粗細)
        elif corners == 4:
            cv2.putText(imgContour, 'rectangle', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif corners == 5:
            cv2.putText(imgContour, 'pentagon', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif corners >= 6:
            cv2.putText(imgContour, 'circle', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            


cv2.imshow('img', img)
cv2.imshow('canny', canny)
cv2.imshow('imgContour', imgContour)
cv2.waitKey(0)