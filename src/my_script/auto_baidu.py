# coding=utf-8

import time
import subprocess
import re


def self_continue_download(path):
    """
    中断恢复地下载baidu资源

    :param path: 云盘内路径，支持文件，文件夹，例如'/df/濡鸦之巫女'
    """
    file_name_old = 'bai.log'
    while True:
        # 检查是否存在BaiduPCS-Go进程
        re_grep = subprocess.run(['ps -ef | grep BaiduPCS | grep -v grep'], shell=True, stdout=subprocess.PIPE)
        print(f'[auto_baidu] re_grep={re_grep}')
        # 如果存在
        if re_grep.returncode == 0:
            # 拿到stdout转成str
            stdout_str = str(re_grep.stdout, encoding='utf-8')
            # 按行分开
            for line in stdout_str.split('\n'):
                print(f'[auto_baidu] line={line}')
                # 空行过滤
                if len(line) != 0:
                    # 按字段隔开
                    fields = re.split(' +', line)
                    print(f'[auto_baidu] fields={fields}')
                    # kill相应进程号
                    re_kill = subprocess.run(f'kill {fields[1]}', shell=True)
                    print(f'[auto_baidu] re_kill={re_kill}')
        # 检查是否下载完成
        with open(f'{file_name_old}', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) > 0 and lines[len(lines) - 1].startswith('任务结束'):
                break
        # 启动
        subprocess.run(f'nohup ./BaiduPCS-Go d {path} --save --locate -p 1 -l 1 >{file_name_old} 2>&1 &', shell=True)
        # 休眠1小时
        time.sleep(60 * 60)
    print("[auto_baidu] job finished")
    # 移动日志文件
    file_name_new = file_name_old + '.' + path[path.rindex('/') + 1:]
    subprocess.run(f'mv {file_name_old} {file_name_new}', shell=True)


self_continue_download('/df/摩登大圣动画版')
