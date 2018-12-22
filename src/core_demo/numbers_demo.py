# python3有3种数字类型：整型(integer)，浮点(float)，复数(complex)
# 都是对象，不可变

import decimal
import fractions
import sys

# python3整形没有范围，只要内存够
# bit_length可变，和8没关系
num = 123456
print(num.bit_length())

# 其他进制
x = 0b101
y = 0o123
z = 0x10

# 类型判断
isinstance(2.2, float)

# // 返回商数
# % 返回余数
# 返回两者
divmod(7, 2)

# 转型
int()
float()
complex()

# 字符 -> 数字
print(ord('a'))

# float默认精度为15位
print(sys.float_info)
print(sys.float_info.dig)
# 存在常见float问题
print('float常见问题，1.1 + 2.2 = ' + str(1.1 + 2.2))

""" decimal """
# 解决float误差
decimal.Decimal('0.12')
decimal1 = decimal.Decimal('1.1') + decimal.Decimal('1.2')
print('decimal1 = ' + str(decimal1))
# 解决float精度
decimal2 = decimal.Decimal('0.123456789_0123456789_0123456789')
decimal3 = decimal.Decimal('0.111111111_1111111111_1111111111')
decimal4 = decimal2 - decimal3
print('decimal4 = ' + str(decimal4))
decimal.getcontext().prec = 2
decimal4 = decimal2 - decimal3
print('decimal4 = ' + str(decimal4))

""" fractions """
fractions1 = fractions.Fraction(2.5)
fractions2 = fractions.Fraction(1, 3)
print(fractions1)
print(fractions2)

""" 常见numbers built-in function """
abs(-1)
max(1, 2, 3)
min(1, 2, 3)
round(3.1415, 2)
# 不建议使用的round(3.1415, -1)
