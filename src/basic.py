# -*- coding: utf-8 -*-

"""if """
x = int(input('Please enter an integer'))
if x < 0:
    x = 0
    print('Negative changed to zero')
elif x == 0:
    print('Zero')
elif x == 1:
    print('Single')
else:
    print('More')

""" for """
# 对于list的迭代，如果要修改list的内容，建议先复制，[:]符号在此特别方便
words = ["a", "b", "c", "d"]
for w in words[:]:
    if len(w) > 6:
        words.insert(0, w)
# 如果没有片操作，代码生成无限list

""" range """
# python中for循环不迭代数字，如果要，使用range
for i in range(5):
    print(i)
# 5, 6, 7, 8, 9
range(5, 10)
# 0, 3, 6, 9
range(0, 10, 3)
# -10, -40, -70
range(-10, -100, -30)

# 如果要迭代数组下标，可以使用for与range
a = ['Mary', 'had', 'a', 'little', 'lamb']
for i in range(len(a)):
    print(i, a[i])
# 这些情况用enumerate() 最方便
# print(range(10))不返回数组，而是对象，只在迭代时生成各item，并不生成list，这种对象被称为iterable
# for循环可以接收iterable，list()也可以

""" break """
# 跳出最近的for和while

""" loop中的else """
# 只在for迭代完成或while条件不成立时执行，break不执行
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n // x)
            break
    else:
        print(n, 'is a prime number')

""" pass """
# 空命令，语法需要但不用做任何事时使用，coding时可以先写上，之后再实现相应功能

""" 定义函数 """


def fib(n):
    """Print a Fibonacci series up to n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a + b
    print()


# def指函数定义，函数体在下行开始，必须缩进
# 函数体首行可以是字符串常量，作为函数文档
# 全局变量不能在函数中赋值，除非使用global
# 定义的函数名可以赋值给新变量
f = fib


# 没有返回值的函数会返回内建的值，None
# in的一种判断用法
# if ok in ('y', 'ye', 'yes'):


# 可定义参数默认值，默认值可用变量
# 默认参数只处理一次
def f(a, L=[]):
    L.append(a)
    return L


# [1]
print(f(1))
# [1, 2]
print(f(2))
# [1, 2, 3]
print(f(3))


# 如果不想在调用间共享，可如下定义
def f(a, L=None):
    if L is None:
        L = []
    L.append(a)
    return L


# 调用时，可以指定参数名并传值
# ** name形式的参数可以接受一个dictionary
# *name可变参数，接受tuple，在range()
# 中也可以使用range(*args)


""" 文档描述 """
# 首先必须是精简的描述，以动词开关，.结尾
# 如果有多行，第二行必须是空行
# 对齐问题参考https: // docs.python.org / 3 / tutorial / controlflow.html  # documentation-strings
# print(my_function.__doc__)
# 查看函数文档描述

""" list操作 """
squares = []
for x in range(10):
    squares.append(x ** 2)
# 生成list后还会有x变量残留
# 用squares = list(map(lambda x: x ** 2, range(10)))
# 或squares = [x ** 2 for x in range(10)]
# 可以达到相同效果，且没有x留下
# 这种用[]，for ，if创建数组的方法叫list comprehension
# zip()# ，二维list行列转换
# del ()
# 用下标删除元素，或片，或删除变量
# tuples和sequences
# list, tuple, range都是sequence类型
# tuple是用, 分隔的一些值，t = 12345, 54321, 'hello!'，三个项目被pack到t中作为tuple
# tuple不可变
# x, y, z = t，t被unpack成3个项目
# Note that multiple assignment is really just a combination of tuple packing and sequence unpacking.
