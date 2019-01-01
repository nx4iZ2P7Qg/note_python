# 序列化

# pickle模块处理
# pickle可扩展，跨版本，但对错误或者恶意构建的结构来说，不是非常安全

# pickle可以储存的类型
# python维护的本地类型
# Booleans, integers, floating point numbers, complex numbers, strings, bytes objects, byte arrays, and None
# 本地类型的list, tuple, dictionary, set
# 函数, 类, 实例(有限制的)

# 使用
# 创建对象
website = {'title': 'Techbeamers', 'site_link': '/', 'site_type': 'technology blog',
           'owner': 'Python Serialization tutorial', 'established_date': 'Sep2015'}

import pickle

with open('website.pickle', 'wb') as f:
    pickle.dump(website, f)

# 文件是以wb(二进制读写)模式使用的
# pickle是以python为中心的，不保证跨语言兼容

# 读取
import pickle

with open('website.pickle', 'rb') as f:
    data = pickle.load(f)
    print(data)
