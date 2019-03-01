# 待转换字符串
camel_case_str = 'notificationTypes'
# 第一个字符转换
re_str = camel_case_str[0].lower()
# 其他字符转换
for i in range(1, len(camel_case_str)):
    tmp = camel_case_str[i]
    if tmp.isupper():
        re_str += '_' + tmp.lower()
    else:
        re_str += tmp
print(re_str)