import subprocess
import requests

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
    return 0, grep_result


def send_to_gotify(url, message):
    data = {'title': '硬盘关键 smart', 'message': f'{message}', 'priority': '10'}
    requests.post(f'{url}', data=data, verify=False)


for attribute in attributes:
    c, m = grep_str_in_file(attribute, smart_file)
    if c == 0:
        line_arr = m.decode('utf-8').split('\n')
        # 最后一个元素是 ''，输出最后一个有意义的行
        m = line_arr[-2]
        send_to_gotify(smart_url, m)
