import requests
import re
import codecs

import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


def jav_black_pic_ocr(pic_path, step):
    """
    从jav取得的黑底图片中识别文件大小

    :param pic_path: 图片路径
    :param step: 100*25扫描框向下移动像素数
    :return: 相应字符串
    """
    img = Image.open(pic_path)
    for i in range(0, 100, step):
        # 裁剪长100，宽25的区间，以方便识别
        temp = img.crop((0, 50 + i, 100, 75 + i))
        # 放大图片，提高识别度
        temp = temp.resize((300, 75), Image.ANTIALIAS)
        temp.save("d:/download/test.jpg")
        text = pytesseract.image_to_string(temp)
        if 'Size' in text:
            return 0, text
    else:
        return 1, None


# ocr 参考 https://blog.csdn.net/jclian91/article/details/80628188

# headers = {
#     'User-Agent':
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
#     "Host": "www.javjunkies.com",
#     "Upgrade-Insecure-Requests": "1",
#
# }
response = requests.get('http://www.javjunkies.com/main/2019/07-05-10/')
# cookies = response.cookies
# print(cookies)
html = response.content.decode('utf-8')
print(html)

black_pic_list = re.findall('<script>document.write[(]unescape[(]"(.*)"[)][)]</script>', html)
size_list = []
# for i in range(len(black_pic_list)):
#     # print(f'pic = {page_unicode_pic}')
#     unicode_str = black_pic_list[i].replace('%', '\\')
#     link = codecs.decode(unicode_str, 'unicode_escape')
#     link = 'http://javjunkies.com/main/ij/i/' + link[link.rindex('=') + 1:-2] + '.png'
#     # print(f'link = {link}')
#     response = requests.get(link)
#     with open(f'd:/download/{i}.jpg', 'wb') as jpg:
#         jpg.write(response.content)
#         # 尝试各种step
#         for step in [10, 1]:
#             re, text = jav_black_pic_ocr(f'd:/download/{i}.jpg', step)
#             print(f'i={i} step={step} {re} {text}')
#             if re == 0:
#                 text = text[text.index(' ') + 1:text.rindex('GB')]
#                 size_list.append(text)
#                 break
#         else:
#             print(f'black_pic_list[{i}] not recognized')
print(size_list)


class Jav:
    def __init__(self, size, torrent_link, pic_path):
        self.size = size
        self.torrent_link = torrent_link
        self.pic_path = pic_path
