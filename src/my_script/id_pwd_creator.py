# coding=utf-8
import random

__author__ = 'DF'

# 密码安全原则
# 注意问题
#   钓鱼（不明邮件，网站）
#   暴力破解
#   雷达（输入密码的时候，要注意周围）
#   键盘记录程序
# 好密码
#   至少8位包含大小写字母，数字，符号（建议12位）
#   不要包含单词
#   不同的网站用不同的密码，并且没有任何关系
#   不要包含用户名，公司名，或真实的名字
#   使用密码的时候，要注意是否HTTPS等加密连接
#   不要让别人知道密码
#   不要用别人的电脑登录
#   经常更换密码
#   需要一个安全的软件来储存你的密码

# 数字
numList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# 符号
syntaxList = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+',
              '[', '{', ']', '}', '\\', '|', ';', ':', '\'', '\"', ',', '<', '.', '>', '/', '?']
# 字母
charList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
            'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
# 用户名首字母
randomNameFirstList = ['_'] + charList
# 用户名字符
randomNameList = numList + ['_'] + charList
# 密码字符
randomPwdList = numList + syntaxList + charList
i = 0
# 返回id
reId = ''
while i <= random.randint(6, 10):  # 生成6-10位随机的ID
    if i == 0:
        reId = str(randomNameFirstList[random.randint(0, len(randomNameFirstList) - 1)])
    else:
        reId += str(randomNameList[random.randint(0, len(randomNameList) - 1)])
    i += 1
print(reId)
i = 0
# 返回pwd
rePwd = ''
while i <= random.randint(10, 12):  # 生成6-10位随机的密码
    rePwd += str(randomPwdList[random.randint(0, len(randomPwdList) - 1)])
    i += 1
print(rePwd)
