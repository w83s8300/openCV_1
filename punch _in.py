import cv2
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from PIL import Image
import pytesseract
import numpy as np
import random
import matplotlib.pyplot as plt
import ddddocr
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select   # 使用 Select 對應下拉選單

def cv_imread(image_path):
    image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
    image = cv2.resize(image,(540,300))#放大
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    # image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
    # image = cv2.resize(image, (0, 0), fx=1.0, fy=1.0, interpolation=cv2.INTER_CUBIC)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image = cv2.adaptiveThreshold(image,255,1,1,11,2)
    # image = cv2.medianBlur(image, 5)   # 模糊化
    # image=cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # image = cv2.GaussianBlur(image, (25, 25), 0) # 指定區域單位為 (25, 25)
    
    return image
# 计算邻域非白色个数
def calculate_noise_count(img_obj, w, h):
    """
    计算邻域非白色的个数
    Args:
        img_obj: img obj
        w: width
        h: height
    Returns:
        count (int)
    """
    count = 0
    width, height,s = img_obj.shape
    for _w_ in [w - 1, w, w + 1]:
        for _h_ in [h - 1, h, h + 1]:
            if _w_ > width - 1:
                continue
            if _h_ > height - 1:
                continue
            if _w_ == w and _h_ == h:
                continue
            if (img_obj[_w_, _h_,0] < 233) or (img_obj[_w_, _h_,1] < 233) or (img_obj[_w_, _h_,2] < 233):
                count += 1
    return count


# k邻域降噪
def operate_img(img,k):
    w,h,s = img.shape
    # 从高度开始遍历
    for _w in range(w):
        # 遍历宽度
        for _h in range(h):
            if _h != 0 and _w != 0 and _w < w-1 and _h < h-1:
                if calculate_noise_count(img, _w, _h) < k:
                    img.itemset((_w,_h,0),255)
                    img.itemset((_w, _h,1), 255)
                    img.itemset((_w, _h,2), 255)

    return img
def show_img(name, image):
    cv2.imshow(name, image)
    cv2.waitKey(0)
def cv_save(image, result_path):
    cv2.imencode('.png', image)[1].tofile(result_path)    
if __name__ == '__main__':
    id='w83s8300'
    password='q83a8300'
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)  #不自动关闭浏览器
    # options.add_argument('--start-maximized')#浏览器窗口最大化
    driver=webdriver.Chrome(options=options)
    driver.get('https://leeten.loc.com.tw/')
    time.sleep(3)
    # 讀取元素
    element = driver.find_element("name", "ID")
    # 輸入文字
    element.send_keys(id)
    # 讀取元素
    element = driver.find_element("name", "PWD")
    # 輸入文字
    element.send_keys(password)
    # 找到所有img元素
    imgs = driver.find_elements(by="xpath", value="//img")

    # 獲取包含RandomPic.jsp的圖片
    for img in imgs:
        src = img.get_attribute("src")
        if "RandomPic.jsp" in src:
            # 獲取截圖
            screenshot = img.screenshot_as_png

            # 將截圖保存到本地
            with open("kaptcha.png", "wb") as f:
                f.write(screenshot)

    # # # 關閉瀏覽器
    # # driver.quit()
    # # # 獲取截圖
    # # screenshot = img.screenshot_as_png


    # # element = driver.find_element("name", "xRP")
    # # element.screenshot("kaptcha.png")
    

    ##辨識驗證碼###
    # pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    result_path = ''
    front_path = './kaptcha.png'
    back_path = './grassland.jpg'
    #處理圖片
    image = cv2.imread(front_path)##載入圖片
    image= cv2.resize(image, (0, 0), fx=4.0, fy=4.0, interpolation=cv2.INTER_CUBIC)#放大
    # gray = cv2.fastNlMeansDenoisingColored(image, None, 10, 3, 3, 3)
    lower = np.array([0, 0, 175])
    upper = np.array([255, 255, 255])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)#變灰
    mask = cv2.inRange(hsv, lower, upper)#去背
    cv_save(mask, result_path + 'kaptcha-1.png')#處存
    # img = Image.open('kaptcha-1.png')#載入圖片
    # text = pytesseract.image_to_string(img, lang='eng')#辨識
    ocr=ddddocr.DdddOcr()
    with open('kaptcha-1.png','rb')as f:
        img_bytes=f.read()
        text=ocr.classification(img_bytes)
    print("text="+text)
    # 讀取元素
    element = driver.find_element("name", "ImageKey")
    # 輸入文字
    element.send_keys(text)
    driver.find_element("name", "Submit").click()
    # iframe 直接切換到iframe裡的框架
    driver.get('https://leeten.loc.com.tw/Modules/PWC_OnlineCard/OnlineCard.jsp')# 使用 get 方法
    #找到下拉式選單元素
    select_element = driver.find_element(By.NAME, 'CI_Class')
    select = Select(select_element)
    option_list = select.options
    # select.select_by_value('3')
    driver.find_element("id", "go").click() #打卡
    driver.switch_to.alert.accept()
    
    