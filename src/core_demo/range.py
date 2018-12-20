# python中for循环不迭代数字，如果要，使用range
for i in range(5):
    print(i)

# 不返回数组，而是对象，只在迭代时生成各item，并不生成list，这种对象被称为iterable
print(range(10))

# 5, 6, 7, 8, 9
range(5, 10)
# 0, 3, 6, 9
range(0, 10, 3)
# -10, -40, -70
range(-10, -100, -30)

# 类似函数可变形参个数的用法
variable_length_arg = 1, 10
for x in range(*variable_length_arg):
    print(x, end=' ')
