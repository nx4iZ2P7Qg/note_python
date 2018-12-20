import os
from pathlib import Path

# 处理javjunkies网站上的种子文件
# 有时种子文件第一个byte是无意义字符，会影响torrent的解析

# 种子目录
file_path = Path('.')
# 遍历待处理种子目录
torrents_list = os.listdir(file_path)
# 过滤掉非种子文件
torrents_list = [x for x in torrents_list if x[-8:] == '.torrent']
# 处理后种子目录
finished_torrent_path = Path('./new_torrent')
for i in range(0, len(torrents_list)):
    # 原文件
    file = open(file_path / torrents_list[i], 'br+')
    # 新文件
    file_new = open(finished_torrent_path / torrents_list[i], 'bw+')
    # 跳过有问题的字节
    file.seek(1)
    # 写入新文件
    file_new.write(file.read())
    file.close()
    file_new.close()
