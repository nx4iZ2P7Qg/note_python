# coding=utf-8

"""
实际coding
    Fibonacci数列问题

    python和c一样，非0整数为true，0为false，也可以为字符串或数组，长度非0为true，长度0为false
    可以将结果输出在一行
"""
a, b = 0, 1
while b < 10:
    print(b)
    a, b = b, a + b
print(b, end=',')
