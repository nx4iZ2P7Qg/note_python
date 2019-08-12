import pyautogui
import pytesseract
import time
from PIL import Image

# 1600 * 900
nekopara_vol_1 = {
    'title': 'ネコぱら vol.1',
    'sub_area': [(326, 787, 1316, 937), (326, 827, 1316, 977)],
    'threshold': 210,
    'resize': 0.3,
}

# 1600 * 900
nekopara_vol_2 = {
    'title': 'ネコぱら vol.2',
    'sub_area': [(326, 787, 1316, 937)],
    'threshold': 220,
    'resize': 0.3,
}

# 窗口大小及位置默认
evenicle_2 = {
    'title': 'イブニクル２',
    'sub_area': [(526, 1227, 1826, 1477), (216, 1367, 1876, 1527)],
    'threshold': 100,
    'resize': 0.52,
}


def text_ocr(profile):
    # print(pyautogui.getAllTitles())
    win_list = pyautogui.getWindowsWithTitle(profile['title'])
    if len(win_list) != 1:
        print('window not unique')
        return -1
    for win in win_list:
        win.activate()
        time.sleep(0.3)
        for area in profile['sub_area']:
            pic = pyautogui.screenshot(region=(win.left, win.top, win.width, win.height))
            pic = pic.crop(area)
            # threshold
            pic = pic.point(lambda p: p > profile['threshold'] and 255)
            # Tesseract works best on images which have a DPI of at least 300 dpi
            new_width = int(pic.width * profile['resize'])
            new_height = int(pic.height * profile['resize'])
            pic = pic.resize((new_width, new_height), Image.ANTIALIAS)
            pic.save(f'z:/tmp/{area}.jpg')
            pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
            config = r'--psm 3'
            # config = r'--psm 6'
            text = pytesseract.image_to_string(pic, lang='jpn', config=config)
            print(f'----- {area} -----')
            print(f'{text}\n')


text_ocr(evenicle_2)
