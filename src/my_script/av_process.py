# coding=utf-8

import os
import random
import re
import subprocess
import sys
import time

import requests

timeout = 5


def extract_secret(file_name):
    """
    从文件名中提取车牌

    :param file_name: 含车牌的文件名串
    :return: 车牌
    """
    secret_list = re.findall('([a-zA-Z0-9]{2,8}-[0-9]{3,5})', file_name)
    if len(secret_list) > 1:
        print(secret_list)
        raise Exception('找到多个车牌')
    if len(secret_list) < 1:
        raise Exception('找不到车牌')
    secret = secret_list[0].upper()
    return secret


def py_mv(target_dir, file_name, secret_index):
    """
    修改文件名

    :param target_dir: 指定目录
    :param file_name: 源文件名
    :param secret_index: 车牌+索引
    :return: 无
    """
    old_name = file_name
    new_name = secret_index + file_name[file_name.rindex('.'):]
    if old_name == new_name:
        print(f"same file name, mv skip {file_name}")
        return
    subprocess.run(['mv',
                    '-i',
                    target_dir + '/' + old_name,
                    target_dir + '/' + new_name
                    ])


def normalize_file_name(target_dir):
    """
    将无规则的文件名调整为稍有规则

    :param target_dir: 目标目录
    :return: 无
    """
    file_list = os.listdir(target_dir)
    # 去除jpg文件
    file_list = [x for x in file_list if not x.endswith('.jpg')]
    for file in file_list:
        # 若有多个-
        if file.count('-') > 1:
            print(f'multi - found in {file}')
            # 将secret以外的-转换成_
            secret = extract_secret(file)
            secret_index = file.upper().index(secret)
            pre = file[:secret_index].replace('-', '')
            post = file[secret_index + len(secret):].replace('-', '')
            subprocess.run(['mv',
                            target_dir + '/' + file,
                            target_dir + '/' + pre + file[secret_index: secret_index + len(secret)] + post
                            ])
    # 统计分段文件secret
    split_secret = {}
    for file in file_list:
        secret = extract_secret(file)
        if secret not in split_secret:
            split_secret[secret] = 1
        else:
            split_secret[secret] += 1
    print(f'split_secret = {split_secret}')
    for file in file_list:
        print(f'processing file = {file}')
        secret = extract_secret(file)
        # 分段视频
        if split_secret[secret] > 1:
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
            # 没有标注认为是第一段
            else:
                print('_x not matched, processed as first')
                py_mv(target_dir, file, secret)
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


def py_chown(file):
    """
    修改文件用户，组

    :param file: 指定文件
    :return: 无
    """
    subprocess.run(['chown', 'root:root', file])


def py_chmod(file):
    """
    修改文件权限

    :param file: 指定文件
    :return: 无
    """
    subprocess.run(['chmod', '644', file])


def get_pic_by_secret_mstage(secret, target_dir='.'):
    """
    根据车牌号获取相应图片，www.mgstage.com

    :param secret: 车牌号
    :param target_dir: 目录
    :return: 0-正常，1-文件已存在
    """
    secret = secret.upper()
    if '-' not in secret:
        raise Exception('not a valid secret, - not exist')
    if os.path.exists(os.path.join(target_dir, f'{secret}.jpg')):
        raise Exception('pic exist')
    split = secret.split('-')
    if not split[0].isalnum() or not split[1].isdigit():
        raise Exception('not a valid secret, secret split check fail')
    # 各车牌路径，未来可能需要修改结构
    path_dict = {
        '259LUXU': 'luxutv',
        '261ARA': 'ara',
        '300MAAN': 'prestigepremium',
        '300MIUM': 'prestigepremium',
        '300NTK': 'prestigepremium',
        '336KNB': 'kanbi',
        'ABP': 'prestige',
        'ABS': 'prestige',
        '314KIRAY': 'kiray'
    }
    if split[0] in path_dict.keys():
        # 'https://image.mgstage.com/images      /luxutv               /259luxu   /1007/pb_e_259luxu-1007.jpg'
        # 'https://image.mgstage.com/images      /ara                  /261ara    /331 /pb_e_261ara-331.jpg'
        # 'https://image.mgstage.com/images      /prestigepremium      /300maan   /341 /pb_e_300maan-341.jpg'
        # 'https://image.mgstage.com/images      /kiray                /314kiray  /096 /pb_e_314kiray-096.jpg'
        link = f'https://image.mgstage.com/images/{path_dict[split[0]]}/{split[0].lower()}/{split[1].lower()}' \
            f'/pb_e_{secret.lower()}.jpg'
        print(f'get_pic_by_secret_mstage-link = {link}')
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
        }
        response = requests.get(link, headers=headers, timeout=timeout)
        # 图片超过50KB被认为是有效图片
        if len(response.content) > 50_000:
            with open(f'{target_dir}/{secret}.jpg', 'wb') as jpg:
                jpg.write(response.content)
    else:
        raise Exception('get_pic_by_secret_mstage-link not a mstage link')


def get_pic_by_secret_dmm(secret, target_dir='.'):
    """
    根据车牌号获取相应图片，www.dmm.co.jp

    :param secret: 车牌号
    :param target_dir: 目录
    :return: 0-正常，1-文件已存在
    """
    secret = secret.upper()
    if '-' not in secret:
        raise Exception('not a valid secret, - not exist')
    if os.path.exists(os.path.join(target_dir, f'{secret}.jpg')):
        raise Exception('pic exist')
    split = secret.split('-')
    if not split[0].isalnum() or not split[1].isdigit():
        raise Exception('not a valid secret, secret split check fail')
    temp = secret.replace('-', '').lower()
    if split[0] in ['ABP']:
        #        https://pics.dmm.co.jp/mono/movie/adult/118abp627/118abp627pl.jpg
        link = f'https://pics.dmm.co.jp/mono/movie/adult/118{temp}/118{temp}pl.jpg'
    elif split[0] in ['HODV']:
        #        https://pics.dmm.co.jp/mono/movie/adult/41hodv21008/41hodv21008pl.jpg
        link = f'https://pics.dmm.co.jp/mono/movie/adult/41{temp}/41{temp}pl.jpg'
    elif split[0] in ['MDTM']:
        #        https://pics.dmm.co.jp/mono/movie/84mdtm551r/84mdtm551rpl.jpg
        link = f'https://pics.dmm.co.jp/mono/movie/84{temp}r/84{temp}rpl.jpg'
    elif split[0] in ['SDAB']:
        #        https://pics.dmm.co.jp/mono/movie/adult/1sdab104/1sdab104pl.jpg
        link = f'https://pics.dmm.co.jp/mono/movie/adult/1{temp}/1{temp}pl.jpg'
    elif split[0] in ['STARS']:
        #        https://pics.dmm.co.jp/mono/movie/adult/1stars103tk/1stars103tkpl.jpg
        link = f'https://pics.dmm.co.jp/mono/movie/adult/1{temp}tk/1{temp}tkpl.jpg'
    else:
        #        https://pics.dmm.co.jp/mono/movie/adult/ipx232/ipx232pl.jpg
        link = f'https://pics.dmm.co.jp/mono/movie/adult/{temp}/{temp}pl.jpg'
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }
    print(f'get_pic_by_secret_dmm-link = {link}')
    response = requests.get(link, headers=headers, timeout=timeout)
    # 图片超过50KB被认为是有效图片
    if len(response.content) > 50_000:
        with open(f'{target_dir}/{secret}.jpg', 'wb') as jpg:
            jpg.write(response.content)


def get_pic_by_secret_javbus(secret, target_dir='.'):
    """
    根据车牌号获取相应图片，www.javbus.com

    :param secret: 车牌号
    :param target_dir: 目录
    :return: 0-正常，1-文件已存在
    """
    secret = secret.upper()
    if '-' not in secret:
        raise Exception('not a valid secret, - not exist')
    if os.path.exists(os.path.join(target_dir, f'{secret}.jpg')):
        raise Exception('pic exist')
    split = secret.split('-')
    if not split[0].isalnum() or not split[1].isdigit():
        raise Exception('not a valid secret, secret split check fail')
    bus_link = f'https://www.javbus.com/{secret}'
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }
    print(f'get_pic_by_secret_javbus-bus_link = {bus_link}')
    response = requests.get(bus_link, headers=headers, timeout=timeout)
    html = response.content.decode('utf-8')
    # 多行匹配html
    pic_link = re.search('screencap.*<img src="(.*)" title=.*CC0000', html, flags=re.S)
    if pic_link:
        link = pic_link.group(1)
        print(f'get_pic_by_secret_javbus-link = {link}')
        response = requests.get(link, headers=headers, timeout=timeout)
        # 图片超过50KB被认为是有效图片
        if len(response.content) > 50_000:
            with open(f'{target_dir}/{secret}.jpg', 'wb') as jpg:
                jpg.write(response.content)
    else:
        print(f'get_pic_by_secret_javbus-link re search failed')


def av_process(path=os.getcwd()):
    """
    例行处理视频文件

    要求：若干视频文件存在某一目录下，文件名可以较乱，但要包含带'-'的车牌
    结果：视频命名规整化，下载图片，调整图片mtime与视频相同，处理用户组

    :param path: 指定目录
    :return: 无
    """
    print('------- start -------')

    print('------- normalize_file_name start -------')
    # 规范文件名
    normalize_file_name(path)

    # 用set保存待下载车牌号，避免分段视频重复下载，避免重复下载已存在的jpg
    secret_set = set()
    for file in os.listdir(path):
        secret = extract_secret(file)
        print(f'secret extracted = {secret}')
        # 文件不是jpg，且相应jpg文件不存在
        if not file.endswith('jpg') and not os.path.exists(os.path.join(path, f'{secret}.jpg')):
            secret_set.add(secret)
    print(f'secret_set = {secret_set}')

    print('------- downloading pics start -------')
    # 下载所有车牌对应的图片
    for secret in secret_set:
        print('call mstage')
        try:
            get_pic_by_secret_mstage(secret, target_dir=path)
            continue
        except Exception as e:
            print(f'call mstage failed = {secret}')
            print(e)
        print('call dmm')
        try:
            get_pic_by_secret_dmm(secret, target_dir=path)
            continue
        except Exception as e:
            print(f'call dmm failed = {secret}')
            print(e)
        print('call javbus')
        try:
            get_pic_by_secret_javbus(secret, target_dir=path)
            continue
        except Exception as e:
            print(f'call javbus failed = {secret}')
            print(e)
        # # 随机休眠
        # time.sleep(random.randint(6, 30) / 3)
    print('------- download pics end -------')

    print('------- mtime start -------')
    file_list = os.listdir(path)
    for file in file_list:
        for f in file_list:
            # 修改分段非首段，及.jpg文件的mtime
            if f.startswith(file[:file.rindex('.')]):
                modify_mtime(path, file, f)

    print('------- user_group start -------')
    for file in file_list:
        # 修改用户与组
        py_chown(path + '/' + file)

    print('------- privilege start -------')
    for file in file_list:
        # 修改权限
        py_chmod(path + '/' + file)
    print('------- finished -------')


av_process(sys.argv[1])
