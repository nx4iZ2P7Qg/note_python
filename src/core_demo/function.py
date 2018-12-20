# def指函数定义，函数体在下行开始，必须缩进
# 函数体首行可以是字符串常量，作为函数文档
# 全局变量不能在函数中赋值，除非使用global


def fib(n):
    """
    输出斐波纳契数列，前两个数为0, 1，后面的数是前两个数之和

    :param n: 数列最大值不大于等于n
    :return: None
    """
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a + b


print('fib(10):')
fib(10)
print('\n')

# 定义的函数名可以赋值给新变量，函数引用
f = fib


# 没有返回值的函数，返回内建值None


# 可定义参数默认值，默认值可用变量
# IDE提示默认值最好使用不可变量
# 默认参数只处理一次
def function1(param1, tuple1=('a',)):
    """
    输出默认参数

    :param param1: 参数1
    :param tuple1: 元组1
    :return: list
    """
    list1 = list(tuple1)
    list1.append(param1)
    return list1


print('function1 return = ' + str(function1('b')))


# *name，形参，接受tuple，形参个数可变
def function_tuple(*arg):
    """
    输出元组参数

    :param arg: 元组
    :return: None
    """
    for x in arg:
        print(x)


function_tuple(1, 2, 3)


# **name，可以接受一个dictionary
def function_dictionary(**arg):
    """
    输出字典参数

    :param arg: 字典
    :return: None
    """
    for k, v in arg.items():
        print(k, v)
    for k in arg:
        print(k, arg[k])


function_dictionary(k1='v1', k2='v2')
