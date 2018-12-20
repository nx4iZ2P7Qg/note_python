# coding=utf-8
"""
元组不可变
"""

tuple1 = ()
# 不加逗号会被认为是int
tuple2 = (10,)
tuple3 = ('a', 'b', 'c')
tuple4 = 'a', 'b', 'c'

del tuple1

# 从list转型
list1 = ['a', 'b', 'c']
tuple5 = tuple(list1)
