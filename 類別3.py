import cv2
import numpy
from PIL import Image
img1 = cv2.imread('000.jpeg')
img2 = cv2.imread('shape01.jpg')
img1_pil = Image.fromarray(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)) #转换为PIL格式
img2_pil = Image.fromarray(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
img1_pil.paste(img2_pil, (800, 100)) #img2贴在img1指定位置，位置是(左,上)
img = cv2.cvtColor(numpy.asarray(img1_pil), cv2.COLOR_RGB2BGR) #PIL转换为cv2格式
cv2.imshow('image', img)
cv2.waitKey(0)