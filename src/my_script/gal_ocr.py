import pyautogui
import pytesseract
from PIL import Image

# nekopara_vol_1
# 1600 * 900
# config = {
#     'title': 'ネコぱら vol.1',
#     'sub_area': (326, 787, 1316, 937),
#     'threshold': 210,
# }

# nekopara_vol_2
# 1600 * 900
config = {
    'title': 'ネコぱら vol.2',
    'sub_area': (326, 787, 1316, 937),
    'threshold': 220,
}


def text_ocr():
    win_list = pyautogui.getWindowsWithTitle(config['title'])
    if len(win_list) != 1:
        print('window not unique')
        return -1
    for win in win_list:
        pic = pyautogui.screenshot(region=(win.left, win.top, win.width, win.height))
        pic = pic.crop(config['sub_area'])
        # convert to gray
        # pic = pic.convert('L')
        # threshold
        pic = pic.point(lambda p: p > config['threshold'] and 255)
        pic = pic.resize((pic.width * 3, pic.height * 3), Image.ANTIALIAS)
        # pic.save('z:/tmp/abc.jpg')
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
        # text = pytesseract.image_to_string(pic, config='oem 2', lang='jpn')
        text = pytesseract.image_to_string(pic, lang='jpn')
        print(text)


text_ocr()
