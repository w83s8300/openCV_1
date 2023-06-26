import numpy as np
import random
import cv2

# 讀取中文路徑圖檔，並轉換為BGR
def cv_imread(image_path):
    image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    return image

# 顯示圖檔
def show_img(name, image):
    cv2.imshow(name, image)
    cv2.waitKey(0)

# Numpy儲存中文路徑圖檔
def cv_save(image, result_path):
    cv2.imencode('.jpg', image)[1].tofile(result_path)    
    
# 比例縮小圖檔
def resize_img(image, pos):
    image = cv2.resize(image, dsize=None, fx=pos, fy=pos)
    return image

# 旋轉圖片
def rotate_img(image):
    # 讀取圖片大小
    (h, w, d) = image.shape
    # 找到圖片中心
    center = (w // 2, h // 2)
    # 代表隨機順逆時針旋轉0-2度
    angle = random.randint(-40, 40) / 20
    # 縮放倍數為1.03倍，避免旋轉時小狗圖案被裁切掉
    M = cv2.getRotationMatrix2D(center, angle, 1.04)
    # (w, h )代表圖片縮放與旋轉後，需裁切成的尺寸
    image = cv2.warpAffine(image, M, (w, h))
    return image

# 漫水填充法去背
def image_matting(image):
    h, w = image.shape[:2]
    mask = np.zeros([h + 2, w + 2], np.uint8)
    cv2.floodFill(image, mask, (2, 2), (255, 255, 255), 
                  (130, 130, 130), (50, 50, 50), 
                  cv2.FLOODFILL_FIXED_RANGE)
    return image

# 前後景合成
def prduce_pic(image1, image2, x, y):
    image2_copy = image2.copy()
    # 前景上小狗圖像去背
    image2_copy = image_matting(image2_copy)
    # show_img('floodFill', image2_copy)

    # 前景上產生小狗圖像的mask
    image2gray = cv2.cvtColor(image2_copy, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(image2gray, 254, 255, cv2.THRESH_BINARY)
    # 開運算去除mask中白色雜訊
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # show_img('mask',  mask)

    # 背景上定義小狗ROI區域
    rows, cols, channels = image2.shape
    roi = image1[y:y + rows, x:x + cols]

    # 背景上ROI區域摳出小狗圖案mask
    image1_bg = cv2.bitwise_and(roi, roi, mask=mask)
    # show_img('image1_bg', image1_bg)

    # 前景上產生小狗圖像的inverse mask
    mask_inv = cv2.bitwise_not(mask)
    # show_img('mask_inv', mask_inv)

    # 前景上小狗圖像的inverse mask內填充小狗圖案
    image2_fg = cv2.bitwise_and(image2, image2, mask=mask_inv)
    # show_img('image2_fg', image2_fg)

    # 將「摳出小狗圖案mask的背景」與「填充小狗圖案的前景」相加
    dst = cv2.add(image1_bg, image2_fg)
    # show_img('dst', dst)

    # 用dst替換掉背景中含有小狗的區域
    image1[y:y + rows, x:x + cols] = dst
    # show_img('image1', image1)

    return image1
def empty(v):
    pass
if __name__ == '__main__':
    result_path = './result/'
    front_path = './kaptcha.png'
    back_path = './grassland.jpg'

    front = cv_imread(front_path)
    front = image_matting(front)
    cv2.namedWindow('TrackBar')
    cv2.resizeWindow('TrackBar', 640, 320)

    cv2.createTrackbar('Hue Min', 'TrackBar', 0, 255, empty)
    cv2.createTrackbar('Hue Max', 'TrackBar', 255, 255, empty)
    cv2.createTrackbar('Sat Min', 'TrackBar', 0, 255, empty)
    cv2.createTrackbar('Sat Max', 'TrackBar', 255, 255, empty)
    cv2.createTrackbar('Val Min', 'TrackBar', 0, 255, empty)
    cv2.createTrackbar('Val Max', 'TrackBar', 255, 255, empty)
    h_min = cv2.getTrackbarPos('Hue Min', 'TrackBar')
    h_max = cv2.getTrackbarPos('Hue Max', 'TrackBar')
    s_min = cv2.getTrackbarPos('Sat Min', 'TrackBar')
    s_max = cv2.getTrackbarPos('Sat Max', 'TrackBar')
    v_min = cv2.getTrackbarPos('Val Min', 'TrackBar')
    v_max = cv2.getTrackbarPos('Val Max', 'TrackBar')
    print(h_min, h_max, s_min, s_max, v_min, v_max)
    # show_img('front', front)

    # for i in range(1, 10):
    #     front1 = rotate_img(front)
    #     front1 = resize_img(front1, 0.9615)
    #     back = cv_imread(back_path)
    #     # show_img('back', back)
    #     result = prduce_pic(back, front1, random.randrange(0, 1550), 
    #                         random.randrange(500, 700))
    #     cv_save(result, result_path + str(i) + '.jpg')
    #     print('  成功儲存第 {} 張圖片： {}'.format(i, str(i) + '.jpg'))
    #     print('=' * 50)
    while True:
        show_img('front', front)
        print('※程式執行完畢')