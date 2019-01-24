import requests

# 一般http请求
r01 = requests.get('https://api.github.com/events')
r02 = requests.post('http://httpbin.org/post', data={'key': 'value'})
r03 = requests.put('http://httpbin.org/put', data={'key': 'value'})
r04 = requests.delete('http://httpbin.org/delete')
r05 = requests.head('http://httpbin.org/get')
r06 = requests.options('http://httpbin.org/get')

# 参数传递
payload = {'key1': 'value1', 'key2': 'value2'}
r07 = requests.get('http://httpbin.org/get', params=payload)
print(f'r07.url = {r07.url}')

# 响应内容
# 默认coding
print(r01.encoding)
# 自动decode
print(r01.text)
# 手动decode
print(r01.content.decode('utf-8'))
# 内置json解码器
print(f'r01.json() = {r01.json()}')

# 定制请求头
url = 'https://api.github.com/some/endpoint'
headers = {'user-agent': 'my-app/0.0.1'}
r08 = requests.get(url, headers=headers)

# 表单上传
payload = {'key1': 'value1', 'key2': 'value2'}
r09 = requests.post('http://httpbin.org/post', data=payload)

url = 'https://api.github.com/some/endpoint'
payload = {'some': 'data'}
r = requests.post(url, json=payload)

# Multipart-Encoded
url = 'http://httpbin.org/post'
files = {'file': open('D:/cp_c_cu_1123PM.csar', 'rb')}
r10 = requests.post(url, files=files)
# 显式地设置文件名，文件类型和请求头
url = 'http://httpbin.org/post'
files = {'file': ('report.xls', open('D:/cp_c_cu_1123PM.csar', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
r11 = requests.post(url, files=files)
# 请求中有file filename属性，使用删除filename属性，在特定情况下(flash上传)，才可以拿到123的参数
mano_nsd_files = {
    'tplName': (None, '123'),
    'fileName': ('cp_c_cu_1123PM.yaml', open('D:/cp_c_cu_1123PM.csar', 'r'), 'application/octet-stream'),
}

# 响应状态码
print(f'r01.status_code = {r01.status_code}')

# 响应头
print(f'r01.headers = {r01.headers}')

# cookie
# url = 'http://example.com/some/cookie/setting/url'
# r12 = requests.get(url)
# print(r12.cookies['example_cookie_name'])
# 发送自己的cookie
url = 'http://httpbin.org/cookies'
cookies = dict(cookies_are='working')
r13 = requests.get(url, cookies=cookies)

# 超时
# 所有生产代码都应该使用
# 服务器在 timeout 秒内没有应答，将会引发一个异常（精确地说，是在 timeout 秒内没有从基础套接字上接收到任何字节的数据时）
requests.get('http://github.com', timeout=0.1)
