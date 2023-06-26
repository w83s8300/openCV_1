import cv2
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from PIL import Image
import pytesseract
import numpy as np
import random
import ddddocr
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select   # 使用 Select 對應下拉選單
from selenium.webdriver.common.action_chains import ActionChains #將畫面移動到圖表的位置

def cv_imread(image_path):
    image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
    image = cv2.resize(image,(540,300))#放大
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    return image
# 计算邻域非白色个数
def show_img(name, image):
    cv2.imshow(name, image)
    cv2.waitKey(0)
def cv_save(image, result_path):
    cv2.imencode('.png', image)[1].tofile(result_path)    
if __name__ == '__main__':
    id='superadmin'
    password='adminadmin'
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)  #不自动关闭浏览器
    options.add_argument('--start-maximized')#浏览器窗口最大化
    driver=webdriver.Chrome(options=options)
    driver.get('http://192.168.10.10:33/index_Login.jsp')

    driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/table/tbody/tr/td/div/table[2]/tbody/tr[4]/td[2]/input').click()
    a1 = driver.switch_to.alert  # 通过switch_to.alert切换到alert
    print(a1.text) 
    a1.accept()