# 在众多数据结构中，set可以支持数学操作(并集，交集，差集)
# set内部使用hash table来高效地确定是否包含指定元素

# 空集合
set1 = set()

set2 = {'a', 'b', 'c'}

set2.add('d')
# 批量添加，参数可以是列表，元组，字典
set2.update(('d', 'e', 'f'), ('g',))

set2.remove('a')
# 元素不存在，不会出错
set2.discard('x')
# 随机删除元素
set2.pop()

print('b' in set2)

# 注意set()初始化时，元素为'a' 'b' 'c' ...
set3 = set('123456789')
set4 = set('0_456')
# 差集
print(set3 - set4)
# 并集
print(set3 | set4)
# 交集
print(set3 & set4)
# 对称差集，是这么称呼吗，结果为并集 - 交集，是两个对方集合不存在的元素的并集
print(set3 ^ set4)

# Set comprehension
set5 = {x for x in 'abracadabra' if x not in 'abc'}
set5.clear()

# 子集与超集
set5.issubset(set1)
set5.issuperset(set1)

# frozenset
frozen_set = frozenset(["red", "green", "black"])
