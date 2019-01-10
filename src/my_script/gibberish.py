"""
big5，双字节编码
"""

# 解释三国类游戏乱码的问题

# 较新的三国游戏自定义武将名乱码
# 简体字
gbk_char = '飞'
# 在游戏窗口用普通输入法输入时，汉字以gbk编码的方式保存在磁盘上
temp = gbk_char.encode('gbk')
# 游戏读取自定义名称时，以big解码磁盘数据
temp = temp.decode('big5')
print(temp)

# 更古老的三国游戏乱码问题
# 此处要使用繁体字
big5_char = '趙雲'
# 游戏是繁体中文版，发售时，内部肯定是big5编码
temp = big5_char.encode('big5')
# 在简体操作系统中，会以gbk编码来读取游戏文件
temp = temp.decode('gbk')
print(temp)
