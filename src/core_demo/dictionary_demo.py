# 键必须是不可变的

dic1 = {}
dic2 = {'email': 'fz@', 'pwd': 'z85'}

# 访问
print(dic2['email'])
# .get()，如果不存在key，返回None
print(dic2.get('not_exist'))

# 添加/更新元素
dic2['cell'] = 137

# 迭代
dic2.items()
dic2.keys()
dic2.values()
dic2.pop('email')
# 随机返回
dic2.popitem()

# 删除
del dic2['pwd']
dic2.clear()
del dic2

# 判断相等
# 它会考虑到key的数量，key的名字，每个key对应的值，同时会递归到复杂结构
dic3 = {'a': 'a', 'b': 'b'}
dic4 = {'b': 'b', 'a': 'a'}
print(f'dic3 == dic4: {dic3 == dic4}')

print('email' in dic1)

# dictionary comprehension
print({i: ord(i) for i in ['a', 'b', 'c', 'd', 'e']})
weekdays = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
x1 = {w: len(w) for w in weekdays}
x2 = {w: i for i, w in enumerate(weekdays)}
