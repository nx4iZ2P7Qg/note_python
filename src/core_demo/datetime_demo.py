import datetime
import calendar
import time

# datetime
# 两种类型的date, time对象，naive, aware
# aware，包含时区，用来表示特定的时刻
# naive，只是一种时刻表示，具体的意思由程序来定义
# 需要使用aware对象时，datetime, time对象有可选的时区属性tzinfo
# datetime类只能使用唯一的tzinfo的实现类timezone
# timezone支持简单的时区，复杂时区的支持依赖于程序，因为这是个政治问题
# UTC世界协调时间
print(f'datetime.datetime.utcnow() = {datetime.datetime.utcnow()}')
print(f'datetime.MAXYEAR = {datetime.MINYEAR}')
print(f'datetime.MAXYEAR = {datetime.MAXYEAR}')
# 继承关系
# object
#     timedelta
#     tzinfo
#         timezone
#     time
#     date
#         datetime
ten_days = datetime.timedelta(days=10)
print(f'ten_days.total_seconds() = {ten_days.total_seconds()}')
hundred_days = 10 * ten_days
print(f'hundred_years = {hundred_days}')
ninety_days = hundred_days - ten_days
print(f'ninety_years = {ninety_days}')
# date类型总是naive，这个时间基于Gregorian calendar进行了扩展
print(f'datetime.date.today() = {datetime.date.today()}')
# datetime假设每天都是3600 * 24秒
print(f'datetime.datetime.now() = {datetime.datetime.now()}')
print(f'datetime.datetime.today() = {datetime.datetime.today()}')
# 手动指定时区
print(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))))

# calendar
# 默认周几为一周的开始
print(f'calendar.firstweekday() = {calendar.firstweekday()}')
# 手动设置一周开始
calendar.setfirstweekday(calendar.SUNDAY)
print(f'calendar.isleap(2018) = {calendar.isleap(2018)}')
print(calendar.month(2019, 1))
print(calendar.calendar(2019))

# time
print(f'time.time() = {time.time()}')
