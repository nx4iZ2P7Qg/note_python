import keyword

""" 关键字 """
# keyword模块
print(keyword.kwlist)

""" 标识符 """
# python文档说标识符长度无限，但PEP-8标准要求每行长度最多79字符

# 判断是否关键字
keyword.iskeyword('true')
# 判断是否标识符
'_a4B'.isidentifier()

# 最佳实践
# 类名首字母大写，其他标识符首字母小写
# 私有标识符以_开头
# 不要用_放在标识符开头或结尾，python内部使用了
# 不要使用单一单词标识符
# 可以使用_连接单词


""" 变量 """
# 使用前不需要声明，但要初始化
# 值改变时，python分配一片新内存给变量，旧有内存回收
test = 10
id(test)
test = 11
id(test)
# 一些不可变量会被缓存，比如小整数和字符串
# object是一片内存区域，其中有以下内容
# 值，type designator, 引用数
# object才有类型，变量没有
test = 10
print(type(test))
test = 'tech'
print(type(test))
test = {'Python', 'C', 'Java'}
print(type(test))

""" 缓存 """
test = 'abc'
# 获得变量test的物理地址
id(test)

# python会缓存
# 少于20个字符，没有whitespaces的字符串
# -5 ~ 256之间的整形

# 缓存
s1 = 'ab'
s2 = 'a' + 'b'
print(id(s1) == id(s2))
# 不缓存
s1 = 'a b'
s2 = 'a' + ' ' + 'b'
print(id(s1) == id(s2))

# 结果在范围内
i1 = 256
i2 = 255 + 1
print(id(i1) == id(i2))
# 超出范围
i1 = 257
i2 = 256 + 1
print(id(i1) == id(i2))

""" 文档描述 """
# 首行必须是精简的summary，以动词开头，.结尾
# 如果有多行，第二行必须是空行
# 对齐问题参考https://docs.python.org/3/tutorial/controlflow.html#documentation-strings
# print(my_function.__doc__)查看函数文档描述
