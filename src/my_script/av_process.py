# coding=utf-8

import os
import re
import subprocess
import sys


def extract_av_bangou(file_name):
    """
    从文件名中提取av番号

    :param file_name: 含番号的文件名串
    :return: 番号
    """
    bangou_list = re.findall('([a-zA-Z0-9]{3,6}-[0-9]{3,4})', file_name)
    if len(bangou_list) > 1:
        print(bangou_list)
        raise Exception('找到多个番号')
    if len(bangou_list) < 1:
        raise Exception('找不到番号')
    return bangou_list[0].upper()


def change_filename_to_bangou(target_dir, file_name, bangou_index):
    """
    修改文件名

    :param target_dir: 指定目录
    :param file_name: 源文件名
    :param bangou_index: 番号+索引
    :return: 无
    """
    subprocess.run(['mv',
                    target_dir + '/' + file_name,
                    target_dir + '/' + bangou_index + file_name[file_name.rindex('.'):]
                    ])


def modify_mtime(target_dir, origin_file, modify_file):
    """
    复制指定目录下文件的mtime到另一文件

    :param target_dir: 指定目录
    :param origin_file: 源mtime文件
    :param modify_file: 待修改文件
    :return: 无
    """
    subprocess.run(['touch', '-r',
                    target_dir + '/' + origin_file,
                    target_dir + '/' + modify_file
                    ])


def change_owner(target_dir):
    """
    修改目录下所有文件权限

    :param target_dir: 指定目录
    :return: 无
    """
    for file in os.listdir(target_dir):
        subprocess.run(['chown', 'apache:apache', target_dir + '/' + file])


def av_process(path=os.getcwd()):
    """
    将指定目录下所有文件名类似的文件mtime统一修改为${name}.jpg的日期

    处理的条目为，文件名类似的一组文件
    例aa.mp4，aa.jpg, aa_1.mp4, aa_a.mp4
    :param path: 指定目录
    :return:
    """
    target_dir = path
    print(f'target_dir = {target_dir}')
    change_owner(target_dir)
    # 迭代目标目录下文件
    jpg_file_list = os.listdir(target_dir)
    jpg_file_list = [x for x in jpg_file_list if x.endswith('.jpg')]
    print(f'all .jpg to process = {jpg_file_list}')
    for jpg_file in jpg_file_list:
        bangou = extract_av_bangou(jpg_file)
        print(f'extracted bangou = {bangou}')
        jpg_file_name = jpg_file.replace('.jpg', '')
        video_file_list = [x for x in os.listdir(target_dir) if not x.endswith('jpg') and x.startswith(jpg_file_name)]
        print(f'video_file_list = {video_file_list}')
        for i in range(0, len(video_file_list)):
            modify_mtime(target_dir, jpg_file, video_file_list[i])
            # .mp4改名
            if len(video_file_list) > 1:
                if '_1.' in video_file_list[i] or '_A.' in video_file_list[i] or '_a.' in video_file_list[i]:
                    change_filename_to_bangou(target_dir, video_file_list[i], bangou)
                elif '_2.' in video_file_list[i] or '_B.' in video_file_list[i] or '_b.' in video_file_list[i]:
                    change_filename_to_bangou(target_dir, video_file_list[i], f'{bangou}_2')
                elif '_3.' in video_file_list[i] or '_C.' in video_file_list[i] or '_c.' in video_file_list[i]:
                    change_filename_to_bangou(target_dir, video_file_list[i], f'{bangou}_3')
                elif '_4.' in video_file_list[i] or '_D.' in video_file_list[i] or '_d.' in video_file_list[i]:
                    change_filename_to_bangou(target_dir, video_file_list[i], f'{bangou}_4')
                elif '_5.' in video_file_list[i] or '_E.' in video_file_list[i] or '_e.' in video_file_list[i]:
                    change_filename_to_bangou(target_dir, video_file_list[i], f'{bangou}_5')
                elif '_6.' in video_file_list[i] or '_F.' in video_file_list[i] or '_f.' in video_file_list[i]:
                    change_filename_to_bangou(target_dir, video_file_list[i], f'{bangou}_6')
                elif '_7.' in video_file_list[i] or '_G.' in video_file_list[i] or '_g.' in video_file_list[i]:
                    change_filename_to_bangou(target_dir, video_file_list[i], f'{bangou}_7')
                elif '_8.' in video_file_list[i] or '_H.' in video_file_list[i] or '_h.' in video_file_list[i]:
                    change_filename_to_bangou(target_dir, video_file_list[i], f'{bangou}_8')
                elif '_9.' in video_file_list[i] or '_I.' in video_file_list[i] or '_i.' in video_file_list[i]:
                    change_filename_to_bangou(target_dir, video_file_list[i], f'{bangou}_9')
                else:
                    print('_x not matched, please review code')
            elif len(video_file_list) == 1:
                change_filename_to_bangou(target_dir, video_file_list[i], bangou)
        # .jpg改名
        change_filename_to_bangou(target_dir, jpg_file, bangou)


av_process(sys.argv[1])
