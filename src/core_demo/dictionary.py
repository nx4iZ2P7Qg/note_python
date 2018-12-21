# 键必须是不可变的

dic1 = {}
dic2 = {'email': 'fz@', 'pwd': 'z85'}

# 访问
print(dic2['email'])

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

print('email' in dic1)
