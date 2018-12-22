# 文件命名不要与python内部文件重名
# 比如本文件命名为operator.py，而且文件内使用import命令时

# 逻辑运算符
# and or not
# and or 并不一定返回True, False，但not不同
a = 7
b = 4
print('a and b is', a and b)
print('a or b is', a or b)
print('not a is', not a)

# 位运算符，注意与tuple集合运行的区别
# & | ~ ^ >> <<

# Identity operators
print(type(a) is int)
print((type(b) is not int))

# Membership operators
# in / not in
