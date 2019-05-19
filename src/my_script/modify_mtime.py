import os
import subprocess
import sys


def modify_mtime(path=os.getcwd()):
    """
    将指定目录下所有文件名类似的文件mtime统一修改为${name}.jpg的日期

    处理的条目为，文件名类似的一组文件
    例aa.mp4，aa.jpg, aa_1.mp4, aa_a.mp4
    :param path: 指定目录
    :return:
    """
    target_dir = path
    print(f'target_dir = {target_dir}')
    # 迭代目标目录下文件
    jpg_file_list = os.listdir(target_dir)
    jpg_file_list = [x for x in jpg_file_list if x.endswith('.jpg')]
    print(f'jpg_file_list = {jpg_file_list}')
    for jpg_file in jpg_file_list:
        jpg_file_name = jpg_file.replace('.jpg', '')
        video_file_list = [x for x in os.listdir(target_dir) if not x.endswith('jpg') and x.startswith(jpg_file_name)]
        print(f'video_file_list = {video_file_list}')
        for video_file in video_file_list:
            subprocess.run(['touch', '-r', target_dir + '/' + jpg_file, target_dir + '/' + video_file])

    modify_mtime(sys.argv[1])

