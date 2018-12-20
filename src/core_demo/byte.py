# bytes不可变
# bytes机器可读，string是人类可读
# bytes可直接存储到硬盘，string需要编码
empty_object = bytes(16)
print(type(empty_object))
print(empty_object)
