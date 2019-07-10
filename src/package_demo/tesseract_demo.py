# coding=utf-8

# 安装Tesseract，需要将Tesseract添加到系统变量中，安装时可选支持语言

# Tesseract关于Python的接口 pip install pytesseract

# Python的图片处理模块 pip install pillow

import pytesseract
from PIL import Image

# 若指定路径可不用添加环境变量，cmd下可能需要添加
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
# lang是语言选项
text = pytesseract.image_to_string(Image.open('d:/test.jpg'), lang='chi_sim')

print(text)