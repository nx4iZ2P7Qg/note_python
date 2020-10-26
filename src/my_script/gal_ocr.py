import pyautogui
import pytesseract
import time
from PIL import Image

# 1600 * 900
nekopara_vol_1 = {
    'title': 'ネコぱら vol.1',
    'sub_area': [(326, 787, 1316, 937)],
    # 'sub_area': [(326, 827, 1316, 977)],
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
    # 'sub_area': [(526, 1227, 1826, 1477)],
    'sub_area': [(216, 1367, 2176, 1527)],
    'threshold': 100,
    'resize': 0.26,
}

sabbatOfTheWitch = {
'title': 'サノバウィッチ',
    # 'sub_area': [(526, 1227, 1826, 1477)],
    # 'sub_area': [(216, 1367, 2176, 1527)],
    'sub_area': [(390, 802, 1326, 937)],
    'threshold': 100,
    'resize': 0.25,
}


def text_ocr(profile):
    # print(pyautogui.getAllTitles())
    win_list = pyautogui.getWindowsWithTitle(profile['title'])
    if len(win_list) != 1:
        print('window not unique')
        for win in win_list:
            print(win.title)
        return -1
    for win in win_list:
        win.activate()
        time.sleep(0.1)
        for area in profile['sub_area']:
            print(f'----- {area} -----')
            pic = pyautogui.screenshot(region=(win.left, win.top, win.width, win.height))
            pic = pic.crop(area)
            # threshold
            pic = pic.point(lambda p: p > profile['threshold'] and 255)
            # Tesseract works best on images which have a DPI of at least 300 dpi
            for resize in range(5):
                size = round(resize * 0.1 + profile['resize'], 2)
                print(f'----- {size} -----')
                new_width = int(pic.width * size)
                new_height = int(pic.height * size)
                temp = pic.resize((new_width, new_height), Image.ANTIALIAS)
                # temp.save(f'z:/tmp/ocr/{area}_{size}.jpg')
                # temp.save(f'z:/tmp/ocr/{size}.jpg')
                pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
                config = r'--psm 3'
                # config = r'--psm 6'
                text = pytesseract.image_to_string(temp, lang='jpn', config=config)
                print(f'{text}\n')


text_ocr(nekopara_vol_1)
