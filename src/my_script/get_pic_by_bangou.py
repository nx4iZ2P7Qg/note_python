# coding=utf-8

import re
import requests

a = requests.get("https://www.javbus.com/WANZ-873")
print(a.content.decode('utf-8'))

'https://pics.dmm.co.jp/digital/video/wanz00873/wanz00873pl.jpg'


# links = re.findall('\t\t<a href="(.*.html)">\[' + linkDate[:2] + '-' + linkDate[2:] + '\]', netPageSource)

