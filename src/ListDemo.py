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
"""

list1 = ["a", "b", "c"]
str1 = "d"

list1.append(str1)

list1.extend(["e"])
list1 += ["f"]
list1 *= 2

list1.insert(1, "b")

del list1[1]

list1[1] = "bb"

str2 = list1[2]

list2 = list1.copy()
list3 = list1[:]

list1.sort()
list1.sort(reverse=True)

index1 = list1.index("c", 1)
print("c" in list1)

list1.reverse()

# 统计"c"出现的次数
list1.count("c")
# 清除第一个出现的元素
list1.remove("f")

print("pop = " + list1.pop())
print(list1)

print("len = " + str(len(list1)))

print("max = " + max(list1))

print("min = " + min(list1))


def take_second(elem):
    return elem[1]


list4 = [(1, 2), (1, 4), (1, 1), (1, 3)]
list4.sort(key=take_second)
print(list4)
# 清空
list1.clear()
