import requests
import datetime
import calendar

token_common = 'As2cq6U_LzMViei'
url_common = f'https://oxo.asuscomm.com:3313/message?token={token_common}'


def send_to_gotify(url, title, message):
    data = {'title': f'{title}', 'message': f'{message}', 'priority': '9'}
    requests.post(f'{url}', data=data, verify=False)


today = datetime.date.today()
month = today.month
day = today.day
if day % 7 == 0:
    weeks_in_month = day // 7
else:
    weeks_in_month = day // 7 + 1
weekday = today.weekday()
today_str = today.strftime('%Y-%m-%d')


# 天
if day == 15:
    send_to_gotify(url_common, '小金库', '-')
    send_to_gotify(url_common, '水电费', '-')


# 周
if weekday == calendar.SUNDAY:
    send_to_gotify(url_common, 'nas 备份', '-')
    send_to_gotify(url_common, '游泳', '-')

if weekday == calendar.SUNDAY and weeks_in_month == 2:
    send_to_gotify(url_common, '收集 gal', '-')


# 月
if month % 3 == 0 and day == 1:
    send_to_gotify(url_common, 'nas 数据完整性测试', '-')

if month % 3 == 0 and day == 21:
    send_to_gotify(url_common, '交房租', '3-31，9-30，男')

if (month == 4 or month == 10) and day == 1:
    send_to_gotify(url_common, '换小车雨刷', '-')


# 年
if today_str == '2021-07-10':
    send_to_gotify(url_common, '阳山水蜜桃', '-')

if today_str == '2021-07-21':
    send_to_gotify(url_common, '停车费', '交2个月吧，与房租同步')

if today_str == '2021-09-20':
    send_to_gotify(url_common, '女王生日', '-')
    send_to_gotify(url_common, '威少3年还款事宜', '-')

if today_str == '2021-09-27':
    send_to_gotify(url_common, '小姑生日', '-')

if today_str == '2021-11-14':
    send_to_gotify(url_common, '亲妈生日', '-')
