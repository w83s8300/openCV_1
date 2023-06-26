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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
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
    driver.get('http://192.168.10.10:38/index.jsp')

    # 讀取元素
    element = driver.find_element("name", "UserID")
    # 輸入文字
    element.send_keys(id)
    # 讀取元素
    element = driver.find_element("name", "UserPWD")
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
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
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
    element = driver.find_element("name", "UserImageKey")
    # 輸入文字
    element.send_keys(text)

    driver.find_element("name", "Submit").click()
    # element =driver.find_elements(By.XPATH, '//*[@id="PortalMainMenu"]/div[4]/div/div/nav/ul/li[1]/a/p')
    element =driver.find_element(By.XPATH, '//*[@id="PortalMainMenu"]/div[4]/div/div/nav/ul/li[6]/a').click()
    time.sleep(3)
    element =driver.find_element(By.XPATH, '//*[@id="PortalMainMenu"]/div[4]/div/div/nav/ul/li[6]/ul/li[2]/a').click()
    time.sleep(10)
    element =driver.find_element(By.XPATH, '//*[@id="Modal-ScheduleBoard"]/div/div/div[1]/button').click()
    time.sleep(3)
    element =driver.find_element(By.XPATH, '//*[@id="CarBooking_DomainItemMenu"]/a').click()
    
    time.sleep(3)
    element =driver.find_elements(By.ID, 'CarBookingStage_Eidt')
    Alllen=0
    for i in range(len(element)):
        if element[i].text=='檢視':
            Alllen=Alllen+1
            if Alllen==5:
                js = "window.scrollTo(0, 600);"
                driver.execute_script(js)
                time.sleep(3)
            element[i].click()
            time.sleep(3)
            
            driver.switch_to.frame(driver.find_element("id",'Modal-CarBookingStage_Eidt-Iframe'))
            frameelement =driver.find_elements(By.ID, 'CarBooking_ViewEdit_TabContent')
            for j in range(len(frameelement)):
                print(frameelement[j].text)
            driver.switch_to.default_content()
            driver.find_element(By.XPATH, '//*[@id="Modal-CarBookingStage_Eidt"]/div/div/div[1]/button').click()
            
            time.sleep(3)
            
    element =driver.find_element(By.XPATH, '//*[@id="CarBookingStage_Eidt"]').click()
    
    # time.sleep(3)
    # driver.switch_to.frame(driver.find_element("id",'Modal-CarBookingStage_Eidt-Iframe'))
    # element =driver.find_elements(By.ID, 'CarBooking_ViewEdit_TabContent')
    
    # print(len(element))
    # for i in range(len(element)):
    #     print(i)
    #     print(element[i].text)

    # print('=========================')
    # driver.switch_to.default_content()
    # element =driver.find_element(By.XPATH, '//*[@id="Modal-CarBookingStage_Eidt"]/div/div/div[1]/button').click()
    # driver.switch_to.frame(driver.find_element("id",element[6].get_attribute('id')))
    # print(driver.find_elements(By.CLASS_NAME, 'nav-item'))

    # response = requests.get(driver.current_url)
    # headers = {
    #     # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    #     # "Accept-Encoding": "gzip, deflate",
    #     # "Accept-Language": "en,zh;q=0.9,zh-CN;q=0.8",
    #     # "Cache-Control": "max-age=0",
    #     # "Connection": "keep-alive",
    #     # "Cookie": "PClocationHanzi=%E4%B8%8A%E6%B5%B7_%E4%B8%8A%E6%B5%B7; PClocationNew=SH_2; ttpCityList=shanghai_chengdu_shenzhen_beijing_nanjing_guangzhou_wuhan_tianjin_suzhou_hangzhou_dongguan_chongqing_foshan_ningbo_hefei_qingdao_changsha_xian_zhengzhou_nanning; _ga=GA1.2.1114246023.1555308273; Hm_lvt_339087287c87d6467979b0998d2b8405=1555308267,1556165084; PClocationPinyin=_; 51autoVisitorId=guest%3A036f4599-7178-46a1-8d95-22b7a491614e; cd_sourceId=s-pc-free; cd_switchboard=4000525196; _gid=GA1.2.55365673.1556165085; Hm_lpvt_339087287c87d6467979b0998d2b8405=1556165096",
    #     # "Host": "search.51auto.com",
    #     # "Upgrade-Insecure-Requests": "1",
    #     # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    # }

    # response = requests.get(driver.current_url, headers=headers)
    # driver.get('https://leeten.loc.com.tw/Modules/PWC_OnlineCard/OnlineCard.jsp')
    