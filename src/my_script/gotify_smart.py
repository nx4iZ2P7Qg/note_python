import subprocess
import requests
import datetime

smart_file = '/var/log/daemon.log'
smart_token = 'A61-EfaWFIMejMf'
smart_url = f'https://svrx.asuscomm.com:3313/message?token={smart_token}'

attributes = [
    'Reallocated_Sector_Ct',
    'Reported_Uncorrect',
    'Command_Timeout',
    'Current_Pending_Sector',
    'Offline_Uncorrectable',
]


def grep_str_in_file(string, file):
    try:
        grep_result = subprocess.check_output(f"grep -n '{string}' {file}", shell=True)
    except subprocess.CalledProcessError as e:
        # grep没找到记录时，返回状态1，与其他状态不同，可以认为这是一种正常状态，需要特别处理
        if e.returncode == 1:
            return 1, "找不到相关条目"
        else:
            return e.returncode, e
    message_arr = grep_result.decode('utf-8').split('\n')
    message_arr = [x for x in message_arr if len(x) != 0]
    return 0, message_arr


def send_to_gotify(url, message):
    data = {'title': 'key smart', 'message': f'{message}', 'priority': '10'}
    requests.post(f'{url}', data=data, verify=False)


def filter_message(message_arr):
    filter_arr = []
    for line in message_arr:
        i = str(line).index(' ')
        d = line[i + 1: i + 3]
        h = line[i + 4: i + 6]
        m = line[i + 7: i + 9]
        now = datetime.datetime.now()
        # 保留今天的数据
        if int(d) != now.day:
            continue
        # 计算分钟
        minute_log = int(h) * 60 + int(m)
        minute_now = now.hour * 60 + now.minute
        if minute_now - minute_log <= 30:
            # 保留30分钟内的消息
            filter_arr.append(line)
    return filter_arr


for attribute in attributes:
    c, arr = grep_str_in_file(attribute, smart_file)
    if c == 0:
        re_arr = filter_message(arr)
        if len(re_arr) > 0:
            m = re_arr[-1]
            send_to_gotify(smart_url, m)
