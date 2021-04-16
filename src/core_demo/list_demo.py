# coding=utf-8
"""

可以引用不同的类型，但通常是一致的

支持 indexed 和 sliced 操作

支持slice赋值，如squares[1:3] = [1, 2], squares[1:3] = [];

"""

list1 = ['a', 'b', 'c']
str1 = 'd'

# 添加
list1.append(str1)  # ['a', 'b', 'c', 'd']

# 拼接 list
list1.extend(['e'])     # ['a', 'b', 'c', 'd', 'e']
list1 += ['f']  # ['a', 'b', 'c', 'd', 'e', 'f']
list1 *= 2  # ['a', 'b', 'c', 'd', 'e', 'f', 'a', 'b', 'c', 'd', 'e', 'f']

list1.insert(1, 'b')    # ['a', 'b', 'b', 'c', 'd', 'e', 'f', 'a', 'b', 'c', 'd', 'e', 'f']

# 删除
del list1[1]    # ['a', 'b', 'c', 'd', 'e', 'f', 'a', 'b', 'c', 'd', 'e', 'f']
del list1[1:2]  # ['a', 'c', 'd', 'e', 'f', 'a', 'b', 'c', 'd', 'e', 'f']

# todo 这不是 list 单独的操作
del list1   # not defined

list1 = ['a', 'b', 'c', 'd', 'e', 'f'] * 2  # ['a', 'b', 'c', 'd', 'e', 'f', 'a', 'b', 'c', 'd', 'e', 'f']

# 写
list1[1] = 'bb'     # ['a', 'bb', 'c', 'd', 'e', 'f', 'a', 'b', 'c', 'd', 'e', 'f']

# 读
str2 = list1[2]     # c

# 复制
list2 = list1.copy()
list3 = list1[:]

# 排序
list1.sort()
list1.sort(reverse=True)

# 查找
index1 = list1.index('c', 1)
'c' in list1

# 逆序
list1.reverse()

# 统计'c'出现的次数
list1.count('c')
# 清除第一个出现的元素
list1.remove('f')   # ['a', 'a', 'b', 'bb', 'c', 'c', 'd', 'd', 'e', 'e', 'f']

list1.pop()   # f   ['a', 'a', 'b', 'bb', 'c', 'c', 'd', 'd', 'e', 'e']

len(list1)  # 10

max(list1)  # e

min(list1)  # a


def take_second(elem):
    return elem[1]


# 自定义排序
list4 = [(1, 2), (1, 4), (1, 1), (1, 3)]
list4.sort(key=take_second)     # [(1, 1), (1, 2), (1, 3), (1, 4)]
# 清空
list1.clear()

# 从tuple转型
tuple1 = 'a', 'b', 'c'
list(tuple1)    # ['a', 'b', 'c']

squares1 = []
# 生成list后还会有x变量残留
for x in range(10):
    squares1.append(x ** 2)
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 可以达到相同效果，且没有x留下
squares2 = list(map(lambda xx: xx ** 2, range(10)))

# 这种用[]，for ，if创建数组的方法叫list comprehension
squares3 = [x ** 2 for x in range(10)]

list_of_countries = ["India", "America", "England", "Germany", "Brazil", "Vietnam"]
firstLetters = [country[0] for country in list_of_countries]    # ['I', 'A', 'E', 'G', 'B', 'V']
[x + y for x in 'get' for y in 'set']    # ['gs', 'ge', 'gt', 'es', 'ee', 'et', 'ts', 'te', 'tt']
[x + y for x in 'get' for y in 'set' if x != 't' and y != 'e']   # ['gs', 'gt', 'es', 'et']

# 要同时使用索引与元素，可以使用
for index, element in enumerate(list_of_countries):
    pass

# zip() 二维list行列转换
# zip() 用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象
list6 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
for i in zip(list6[0], list6[1], list6[2]):
    print(i)
