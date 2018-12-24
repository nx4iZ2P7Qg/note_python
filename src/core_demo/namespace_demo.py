# name是object的引用
# namespace是name组成的系统，主要用来防止name冲突
# python用dictionary实现namespace，其中key=name，value=object
# 多个namespace可能有相同的名称，但指向不同对象

# local namespace
# function内部的local name，在调用function时创建，函数返回时释放

# global namespace
# import操作的names，每import一个module，创建一个，程序结束时释放

# built-in namespace
# 内建函数，内建异常，解释器运行时创建，退出时释放


# scope
# 虽然namespace防止了命名的冲突，但我们不能在任意地方随意地使用各name
# python限制了name被特殊规则约束，就是scope
# scope决定了在哪里可以不加前缀地使用name
# python为locals, function, modules, built-ins定义了不同的scope
# local scope就是innermost scope，保存了一份当前方法可用local names的list
# scope for enclosing function，从nearest enclosing scope中开始找name，然后go outwards
# module scope保存了当前module的所有global names
# outermost scope保存了build-in names，这是最后一个search的scope

# scope resolution
# 对于一个name的解析，从innermost开始，一步一步向上层寻找，若找不到抛出NameError
b_var = 10
print("begin()-> ", dir())


def foo():
    b_var = 11
    print("inside foo()-> ", dir())


foo()
print("end()-> ", dir())
# dir()列出所有可用的names

c_var = 5
d_var = 7


def outer_foo():
    global c_var
    c_var = 3
    d_var = 9

    def inner_foo():
        global c_var
        c_var = 4
        d_var = 8
        print('a_var inside inner_foo :', c_var)
        print('b_var inside inner_foo :', d_var)

    inner_foo()
    print('a_var inside outer_foo :', c_var)
    print('b_var inside outer_foo :', d_var)


outer_foo()
print('a_var outside all functions :', c_var)
print('b_var outside all functions :', d_var)

# 如何正确地import module
# from <module name> import *
# 导入所有module的name到当前namespace，但不能确定某些函数是哪个module导入的
print("namespace_1: ", dir())

from math import *

print("namespace_2: ", dir())
print(sqrt(144.2))

from cmath import *

print("namespace_3: ", dir())
print(sqrt(144.2))
# 如果导入的两个module中有相同的函数名，后导入的函数会覆盖之前导入的函数，之前导入的函数不可用，即使用模块名作前缀也不行
# from <module name> import <foo_1>, <foo_2>
# 如果能确定要使用的名称，可以直接导入
# 这种导入方法稍稍好一些，但不能完全防止namespace pollution，因为此module中其他name就无法使用了
# 另外，程序中的相同name也会覆盖module中的name，被影响的方法会dormant(休眠)
# import <module name>
# 这是最可靠和常用的方式
# 问题是在使用相应的name前要加上前缀
# 但可以完全避免namespace pollution，同时可以自由定义name
