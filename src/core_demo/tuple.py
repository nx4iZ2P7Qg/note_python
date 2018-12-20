# coding=utf-8
"""
元组不可变
x, y, z = t，t被unpack成3个项目
Note that multiple assignment is really just a combination of tuple packing and sequence unpacking.

tuple不可变，但内部的元素可能可变
为什么使用元组？
函数返回多个值
元组比list轻量
多个item的容器
可以在dictionary中作为key
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
