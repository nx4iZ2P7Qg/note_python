# coding=utf-8
# @Author DF

import re
import urllib.request
import webbrowser

# 模拟浏览器
headers = ('User-Agent',
           'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
opener = urllib.request.build_opener()
opener.addheaders = [headers]

linkDate = input('input the linkDate: ')

# 1024
url = input("input the linkUrl: ")
netPageSource = opener.open(url).read().decode('utf-8')
links = re.findall('\t\t<a href="(.*.html)">\[' + linkDate[:2] + '-' + linkDate[2:] + '\]', netPageSource)

# cao liu
# url =
# netPageSource = opener.open(url).read().decode('gbk')
# links =

# print(links)

n = 0
print("there are totally " + str(len(links)) + " links")
for link in links:
    webbrowser.open(url[: url.rfind('/') + 1] + link)
    n += 1
    if n % 10 == 0:
        if len(links) % 10 != 0 and input('open another 10 links? y / n\n') == 'y':
            continue
        else:
            break
