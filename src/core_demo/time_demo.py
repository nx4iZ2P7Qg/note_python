# Time和Datetime是python处理时间日期的主要模块
# 在处理日期时间前，需要设置时区

# 重要事项
# time模块含有c运行时库，提供时间控制，它有一些方法可以用来处理系统时间
# 这个模块使用epoch传统，支持时间开始到2038年
# unix的epoch是1970年1月1日0点，各系统的epoch可以使用以下代码确定
import time

time.gmtime(0)
# 术语"Seconds since the Epoch"或者"No. of Ticks since epoch"代表从epoch开始的秒数
# python中的tick是什么意思
# 时间间隔，是浮点数，秒的单位
# 一些方法使用DST格式返回时间(Daylight Saving Time)，是一种机制，夏季时时钟往前调1小时，冬季调回

print(time.time())
localtime = time.localtime(time.time())
# 很重要的结构
print(localtime)

localtime = time.asctime(localtime)
print(localtime)
# 格式化输出
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))
# 将格式字符串转换为时间戳
a = "Sat Mar 28 22:24:24 2016"
print('time.mktime = %s' % time.mktime(time.strptime(a, "%a %b %d %H:%M:%S %Y")))

print('time.clock() = %s' % time.clock())
time.ctime()
time.sleep(1)

import datetime

# 日期加减
dt1 = datetime.datetime(2018, 7, 16)
dt2 = dt1 + datetime.timedelta(days=1)
print('dt2 = %s' % dt2)
print('dt2 - dt1 = %s' % (dt2 - dt1))
