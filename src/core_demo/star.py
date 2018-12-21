""" 解压赋值 """
tuple1 = (4, 5)
x, y = tuple1
# 可作用于任何可迭代对象
string1 = 'abc'
a, b, c = string1
# 这种语法估计不如[]用得多

# 假如有可变长度的数据，比如：姓名、年龄、不确定个数的电话号码
# 如何取得电话部分的数据
# 传统语言可能会跳过前面的下标，然后取电话
# 对于python，使用*
user = [('Ada', 24, '137****1111', '137****2222', '137****3333'), ('Leon', 26, '159****4444')]
for i in user:
    name, age, *cell = i
    print('cell = ' + str(cell))
# 这个过程，类似函数参数个数可变，其中解压出的cell永远是list类型

# 星号解压语法分割字符串
line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false'
user_name, *fields, home_dir, sh = line.split(':')
print(fields)
