import os


def create_directory_if_not_exist(directory_list):
    """
    批量创建文件夹

    :param directory_list: 待创建文件夹路径列表
    """
    for directory in directory_list:
        if not os.path.exists(directory):
            os.makedirs(directory)


dir_list = []

# 下载根目录
download_base_dir = os.path.join(os.path.sep, 'mnt', 'sdb1', 'aria2')

# 下载目录，一定要是机械硬盘
download_dir = os.path.join(download_base_dir, 'downloading')
dir_list.append(download_dir)

# 下载完成目录
download_complete = os.path.join(download_base_dir, 'complete')
dir_list.append(download_complete)

# 日志目录，放在下载目录附近，数据量不小
log_dir = os.path.join(download_base_dir, 'log')
dir_list.append(log_dir)

# 脚本目录
script_dir = os.path.join(os.path.sep, 'home', 'dexter', 'script', 'aria2')

# 种子目录
seeds_dir = os.path.join(script_dir, 'seeds')
dir_list.append(seeds_dir)

# 工作中的种子目录
seeds_work_dir = os.path.join(script_dir, 'seeds_working')
dir_list.append(seeds_work_dir)

# 配置文件目录
conf_dir = os.path.join(os.path.sep, 'etc', 'aria2')
dir_list.append(conf_dir)

# 创建目录
create_directory_if_not_exist(dir_list)

# 自定义日志标识
custom_log = '[df_custom_log]:'
