import ddddocr

ocr=ddddocr.DdddOcr()
with open('kaptcha.png','rb')as f:
    img_bytes=f.read()
    res=ocr.classification(img_bytes)

print(res)