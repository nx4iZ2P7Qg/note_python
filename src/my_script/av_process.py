# coding=utf-8

import os
import random
import re
import subprocess
import sys
import time

import requests


def extract_secret(file_name):
    """
    从文件名中提取车牌

    :param file_name: 含车牌的文件名串
    :return: 车牌
    """
    secret_list = re.findall('([a-zA-Z0-9]{3,7}-[0-9]{3,4})', file_name)
    if len(secret_list) > 1:
        print(secret_list)
        raise Exception('找到多个车牌')
    if len(secret_list) < 1:
        raise Exception('找不到车牌')
    return secret_list[0].upper()


def py_mv(target_dir, file_name, secret_index):
    """
    修改文件名

    :param target_dir: 指定目录
    :param file_name: 源文件名
    :param secret_index: 车牌+索引
    :return: 无
    """
    subprocess.run(['mv',
                    target_dir + '/' + file_name,
                    target_dir + '/' + secret_index + file_name[file_name.rindex('.'):]
                    ])


def normalize_file_name(target_dir):
    """
    将无规则的文件名调整为稍有规则

    :param target_dir: 目标目录
    :return: 无
    """
    file_list = os.listdir(target_dir)
    for file in file_list:
        print(f'processing file = {file}')
        i = 0
        split_flag = False
        for f in file_list:
            # 开始到折线后4位相同，扩展名相同，认为是分段视频
            if f.startswith(file[:file.rindex('-') + 4]) and f.endswith(file[file.rindex('.'):]):
                i += 1
        # 分段视频
        if i > 1:
            split_flag = True
        print(f'split_flag = {split_flag}')
        secret = extract_secret(file)
        print(f'secret extracted = {secret}')
        # 分段视频
        if split_flag:
            if '_1.' in file or '_A.' in file or '_a.' in file:
                py_mv(target_dir, file, secret)
            elif '_2.' in file or '_B.' in file or '_b.' in file:
                py_mv(target_dir, file, f'{secret}_2')
            elif '_3.' in file or '_C.' in file or '_c.' in file:
                py_mv(target_dir, file, f'{secret}_3')
            elif '_4.' in file or '_D.' in file or '_d.' in file:
                py_mv(target_dir, file, f'{secret}_4')
            elif '_5.' in file or '_E.' in file or '_e.' in file:
                py_mv(target_dir, file, f'{secret}_5')
            elif '_6.' in file or '_F.' in file or '_f.' in file:
                py_mv(target_dir, file, f'{secret}_6')
            elif '_7.' in file or '_G.' in file or '_g.' in file:
                py_mv(target_dir, file, f'{secret}_7')
            elif '_8.' in file or '_H.' in file or '_h.' in file:
                py_mv(target_dir, file, f'{secret}_8')
            elif '_9.' in file or '_I.' in file or '_i.' in file:
                py_mv(target_dir, file, f'{secret}_9')
            else:
                print('_x not matched, please review code')
        # 非分段视频
        else:
            py_mv(target_dir, file, secret)


def modify_mtime(target_dir, origin_file, modify_file):
    """
    复制指定目录下文件的mtime到另一文件

    :param target_dir: 指定目录
    :param origin_file: 源mtime文件
    :param modify_file: 待修改文件
    :return: 无
    """
    subprocess.run(['touch',
                    '-r',
                    target_dir + '/' + origin_file,
                    target_dir + '/' + modify_file
                    ])


def py_chmod(file):
    """
    修改目录下所有文件权限

    :param target_dir: 指定目录
    :return: 无
    """
    subprocess.run(['chown', 'root:root', file])


def get_pic_by_secret(secret, target_dir='.'):
    """
    根据车牌号获取相应图片

    :param secret: 车牌号
    :param target_dir: 目录
    :return: 无
    """
    secret = secret.upper()
    # 校验
    split = secret.split('-')
    if '-' not in secret or not split[0].isalnum() or not split[1].isdigit():
        raise Exception('not a valid secret')
    # 各网站路径，未来可能需要修改结构
    path_dict = {
        '259LUXU': 'luxutv',
        '261ARA': 'ara',
        '300MAAN': 'prestigepremium',
        '300MIUM': 'prestigepremium',
        '300NTK': 'prestigepremium',
        '336KNB': 'kanbi',
    }
    # 最终可能有效链接列表
    if split[0] in path_dict.keys():
        split[0] = split[0].lower()
        split[1] = split[1].lower()
        secret = secret.lower()
        # 'https://image.mgstage.com/images      /luxutv               /259luxu   /1007/pb_e_259luxu-1007.jpg'
        # 'https://image.mgstage.com/images      /ara                  /261ara    /331 /pb_e_261ara-331.jpg'
        # 'https://image.mgstage.com/images      /prestigepremium      /300maan   /341 /pb_e_300maan-341.jpg'
        link = f'https://image.mgstage.com/images/{path_dict[split[0]]}/{split[0]}/{split[1]}/pb_e_{secret}.jpg'
    else:
        temp = secret.replace('-', '').lower()
        # 'https://pics.dmm.co.jp/mono/movie/adult/ipx232/ipx232pl.jpg'
        link = f'https://pics.dmm.co.jp/mono/movie/adult/{temp}/{temp}pl.jpg'
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }
    print(f'link 01 = {link}')
    # 随机休眠
    time.sleep(random.randint(6, 30) / 3)
    response = requests.get(link, headers=headers)
    response.raise_for_status()
    # 图片超过50KB被认为是有效图片
    if len(response.content) > 50_000:
        with open(f'{target_dir}/{secret}.jpg', 'wb') as jpg:
            jpg.write(response.content)
            return
    # 少数图片以上地址缺少，比如WANZ-197，下面定义备用地址
    bus_link = f'https://www.javbus.com/{secret}'
    response = requests.get(bus_link, headers=headers)
    html = response.content.decode('utf-8')
    # 多行匹配html
    pic_link = re.search('screencap.*<img src="(.*)" title=.*CC0000', html, flags=re.S)
    if pic_link:
        link = pic_link.group(1)
    print(f'link 02 = {link}')
    response = requests.get(link, headers=headers)
    response.raise_for_status()
    # 图片超过50KB被认为是有效图片
    if len(response.content) > 50_000:
        with open(f'{target_dir}/{secret}.jpg', 'wb') as jpg:
            jpg.write(response.content)
    raise Exception('can\'t find a matching jpg')


def av_process(path=os.getcwd()):
    """
    例行处理视频文件

    要求：若干视频文件存在某一目录下，文件名可以较乱，但要包含带'-'的车牌
    结果：视频命名规整化，下载图片，调整图片mtime与视频相同，处理用户组

    :param path: 指定目录
    :return: 无
    """
    print('start processing file_name')
    # 规范文件名
    normalize_file_name(path)

    # 用set保存待下载车牌号，避免分段视频重复下载
    secret_set = set()
    for file in os.listdir(path):
        secret_set.add(extract_secret(file))
    print(f'secret_set = {secret_set}')

    print('start downloading pics')
    # 下载所有车牌对应的图片
    for secret in secret_set:
        try:
            get_pic_by_secret(secret, target_dir=path)
        except Exception:
            print(f'get pic failed = {secret}')
            continue

    print('start processing mtime')
    file_list = os.listdir(path)
    for file in file_list:
        for f in file_list:
            # 修改分段非首段，及.jpg文件的mtime
            if f.startswith(file[:file.rindex('.')]):
                modify_mtime(path, file, f)

    print('start processing user_group')
    for file in file_list:
        # 修改用户与组
        py_chmod(path + '/' + file)
    print('finished')


av_process(sys.argv[1])
