# coding=utf-8
# http://www.techbeamers.com/python-keywords-identifiers-variables/
import keyword

""" 关键字 """

# 大小写敏感

# 交互模式中输入help进入帮助，输入keywords获得当前版本的关键字

# keyword模块
print(keyword.kwlist)

""" 标识符 """
# python文档说标识符长度无限，但PEP-8标准要求每行长度最多79字符

# 判断是否关键字
print("true is a keyword: " + str(keyword.iskeyword("true")))
# 判断是否标识符
identifierStr = "_a4B"
print(identifierStr + "is a identifier: " + str(identifierStr.isidentifier()))

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
print("old test memory location: " + str(id(test)))
test = 11
print("new test memory location: " + str(id(test)))
# 一些不可变量会被缓存，比如小整数和字符串
# object是一片内存区域，其中有以下内容
# 值，type designator, 引用数
# object才有类型，变量没有
test = 10
print(type(test))
test = "tech"
print(type(test))
test = {"Python", "C", "Java"}
print(type(test))
