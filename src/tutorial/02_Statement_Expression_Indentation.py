test = "abc"
# 获得变量test的物理地址
id(test)

# python会缓存
# 少于20个字符，没有whitespaces的字符串
# -5 ~ 256之间的整形

# 缓存
s1 = "ab"
s2 = "a" + "b"
print(id(s1) == id(s2))
# 不缓存
s1 = "a b"
s2 = "a" + " " + "b"
print(id(s1) == id(s2))

# 结果在范围内
i1 = 256
i2 = 255 + 1
print(id(i1) == id(i2))
# 超出范围
i1 = 257
i2 = 256 + 1
print(id(i1) == id(i2))
