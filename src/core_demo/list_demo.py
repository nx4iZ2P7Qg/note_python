# coding=utf-8
"""
list
可以引用不同的类型，但通常是一致的
squares = [1, 4, 9, 16, 25]
像string和其他所有sequence type一样，支持indexed和sliced操作
squares[:]返回相同的数组
支持拼接，比如squares + [36, 49, 64, 81, 100]
append()在尾部添加新元素
支持slice赋值，如squares[1:3] = [1, 2], squares[1:3] = [];
len()返回长度
可嵌套

list, tuple, range都是sequence类型
"""

list1 = ['a', 'b', 'c']
str1 = 'd'

list1.append(str1)

list1.extend(['e'])
list1 += ['f']
list1 *= 2

list1.insert(1, 'b')

del list1[1]
del list1[1:2]
del list1

list1 = ['a', 'b', 'c', 'd', 'e', 'f'] * 2

list1[1] = 'bb'

str2 = list1[2]

list2 = list1.copy()
list3 = list1[:]

list1.sort()
list1.sort(reverse=True)

index1 = list1.index('c', 1)
print('c' in list1)

list1.reverse()

# 统计'c'出现的次数
list1.count('c')
# 清除第一个出现的元素
list1.remove('f')

print('pop = ' + list1.pop())
print(list1)

print('len = ' + str(len(list1)))

print('max = ' + max(list1))

print('min = ' + min(list1))


def take_second(elem):
    return elem[1]


list4 = [(1, 2), (1, 4), (1, 1), (1, 3)]
list4.sort(key=take_second)
print('sorted list4 = ' + str(list4))
# 清空
list1.clear()

# 从tuple转型
tuple1 = 'a', 'b', 'c'
list5 = list(tuple1)
print('list5 = ' + str(list5))

squares1 = []
# 生成list后还会有x变量残留
for x in range(10):
    squares1.append(x ** 2)
print('squares1 = ' + str(squares1))
# 可以达到相同效果，且没有x留下
squares2 = list(map(lambda xx: xx ** 2, range(10)))
print('squares2 = ' + str(squares2))
# 这种用[]，for ，if创建数组的方法叫list comprehension
squares3 = [x ** 2 for x in range(10)]
print('squares3 = ' + str(squares3))

list_of_countries = ["India", "America", "England", "Germany", "Brazil", "Vietnam"]
firstLetters = [country[0] for country in list_of_countries]
print(firstLetters)
print([x + y for x in 'get' for y in 'set'])
print([x + y for x in 'get' for y in 'set' if x != 't' and y != 'e'])

# 要同时使用索引与元素，可以使用
for index, element in enumerate(list_of_countries):
    print(index, element)

# zip() 二维list行列转换
# zip() 用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象
list6 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
for i in zip(list6[0], list6[1], list6[2]):
    print(i)
