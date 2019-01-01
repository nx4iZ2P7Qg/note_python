import os

# 普通字符串使用8位ASCII储存
# unicode使用16位ASCII储存，使用u标识
print(u'Hello Python!!')

s = 'hello world'
# 句首大写
s.capitalize()
# 大小写转换
s.swapcase()
# 各单词首字母大写
s.title()
s.istitle()
# 在开始结束间统计子串次数
s.count('o', 1, 3)
# 大小写
s.lower()
s.upper()
# 判断是否全小/大写
s.islower()
s.isupper()
# 是否空串
s.isspace()
# 判断是否decimal，特指UNICODE分类中'Nd'下的字符
# 完整列表参考http://www.fileformat.info/info/unicode/category/Nd/list.htm
s.isdecimal()
# UNICODE中Numeric_Type=Digit or Numeric_Type=Decimal
# 完整列表参考http://www.fileformat.info/info/unicode/category/No/list.htm
s.isdigit()
# Numeric_Type=Digit, Numeric_Type=Decimal or Numeric_Type=Numeric
# NI 列表参考http://www.fileformat.info/info/unicode/category/Nl/list.htm
s.isnumeric()
s.isalpha()
s.isalnum()
# tab转space
s.expandtabs(tabsize=4)
# padding，默认用空格填充，可以指定符号
s.rjust(8, '_')
s.ljust(8, '_')
s.center(8, '_')
# 0填充，如果有符号，0在符号后
s.zfill(12)
# 查找，找不到返回-1
s.find('c', 1, 3)
s.rfind('c', 1, 3)
# 定位，找不到抛ValueError
s.index('c', 1, 3)
s.rindex('a', 1, 3)
# 替换，次数可指定
s.replace('a', 'c', 3)
# split，默认以空格分隔，可以指定次数
s.split(' ', 2)
# split line，在行末分隔行，去掉行结束符，如果参数>0，保留行结束符
s.splitlines(True)
# 连接
'__'.join(['a', 'b', 'c'])
# 左右trim，默认处理空白字符
s.lstrip('a')
s.rstrip('b')

# 拼接路径
print(os.path.join('d:', os.path.sep, 'fold', 'sub_fold', 'sub_fold'))

# 格式字符
print("Employee Name: %s,\nEmployee Age:%d" % ('Aisha', 25))
# 完整格式
# %c	character
# %s	string conversion via str() prior to formatting
# %i	signed decimal integer
# %d	signed decimal integer
# %u	unsigned decimal integer
# %o	octal integer
# %x	hexadecimal integer (lowercase letters)
# %X	hexadecimal integer (UPPER-case letters)
# %e	exponential notation (with lowercase ‘e’)
# %E	exponential notation (with UPPER-case ‘E’)
# %f	floating point real number
# %g	the shorter of %f and %e
# %G	the shorter of %f and %E
