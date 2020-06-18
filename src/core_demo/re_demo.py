import re

# 中文字符
#     [\u4e00-\u9fa5]
# 双字节字符
#     [^\x00-\xff]
# 空白行
#     \n\s*\r
# email
#     [\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?
# 网址url
#     [a-zA-z]+://[^\s]*
# 国内电话
#     \d{3}-\d{8}|\d{4}-\{7,8}
# QQ号
#     [1-9][0-9]{4,}
# 邮政编码
#     [1-9]\d{5}(?!\d)
# 18位身份证
#     ^(\d{6})(\d{4})(\d{2})(\d{2})(\d{3})([0-9]|X)$

# 起始位置开始匹配
print(re.match("[a-z]", "1111a2222"))
print(re.match("1111[a-z]", "1111a2222"))

# 扫描整个字符串并返回第一个成功的匹配
# span() 输出下标
print(re.search('com', 'www.aaa.com').span())

line = "a b c d"
reObj = re.search(r' b (.*?) ', line)
print("reObj.group() : ", reObj.group())
print("reObj.group(1) : ", reObj.group(1))

