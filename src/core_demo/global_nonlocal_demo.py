# python引用变量的顺序： 当前作用域局部变量 -> 外层作用域变量 -> 当前模块中的全局变量 -> python内置变量
g_count = 0


def global_test():
    # 要在局部对全局变量修改，需要在局部先声明
    # 如果只读取，就不需要
    global g_count
    g_count += 1
    print(g_count)


global_test()


def make_counter():
    count = 0

    def counter():
        # nonlocal关键字用来在函数或其他作用域中使用外层(非全局)变量
        nonlocal count
        count += 1
        return count

    return counter


def make_counter_test():
    mc = make_counter()
    print(mc())
    print(mc())
    print(mc())


make_counter_test()
