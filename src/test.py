import requests
import re
import codecs

# headers = {
#     'User-Agent':
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
#     "Host": "www.javjunkies.com",
#     "Cookie": "__cfduid=d72866d0fc0e12bb9e93765134854746b1562155287; 43659ab3fe2d4193326216da7aa87ad6=846e824740fc2b43ae5ff61653b8ae63; f71fb716665e6d8d76af8cf70e6f2f60=3bb4b2b00a8fbfe403bf8acabf9b1e2b; 04d5455216b64e358a73658079bea24b=01e3742eb71af302e5e2a211810804bb",
#     "Upgrade-Insecure-Requests": "1",
#
# }
response = requests.get('http://www.javjunkies.com/main/2019/07-08-10/')
# cookies = response.cookies
# print(cookies)
html = response.content.decode('utf-8')
print(html)

# black_pic_list = re.findall('<script>document.write[(]unescape[(]"(.*)"[)][)]</script>', html)
# i = 0
# for page_unicode_pic in black_pic_list:
#     print(f'pic = {page_unicode_pic}')
#     unicode_str = page_unicode_pic.replace('%', '\\')
#     link = codecs.decode(unicode_str, 'unicode_escape')
#     link = 'http://javjunkies.com/main/ij/i/' + link[link.rindex('=') + 1:-2] + '.png'
#     print(f'link = {link}')
#     response = requests.get(link)
#     with open(f'z:/temp/{i}.jpg', 'wb') as jpg:
#         jpg.write(response.content)
#         i += 1
