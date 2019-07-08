# coding=utf-8

import requests
import time
import random


def get_pic_by_bangou(bangou, target_dir='.'):
    """
    根据车牌号获取相应图片

    :param bangou: 车牌号
    :param target_dir: 目录
    :return: 无
    """
    # 各网站路径抽象
    catalog_dict = {
        '259LUXU': 'luxutv',
        '261ARA': 'ara',
        '300MAAN': 'prestigepremium',
        '300MIUM': 'prestigepremium',
        '300NTK': 'prestigepremium',
    }
    # 根据车牌选择目录如果是以下
    for key in catalog_dict.keys():
        prefix = bangou[:bangou.rindex('-')]
        postfix = bangou[bangou.rindex('-') + 1:]
        if prefix == key:
            # 'https://pics.dmm.co.jp/mono/movie/adult/ipx232/ipx232pl.jpg'
            link = f'https://image.mgstage.com/images/{catalog_dict[key]}/{key}/{postfix}/pb_e_{bangou}.jpg'
        else:
            temp = bangou.replace('-', '')
            # 'https://image.mgstage.com/images/luxutv         /259luxu/1007/pb_e_259luxu-1007.jpg'
            # 'https://image.mgstage.com/images/ara            /261ara /331 /pb_e_261ara-331.jpg'
            # 'https://image.mgstage.com/images/prestigepremium/300maan/341 /pb_e_300maan-341.jpg'
            link = f'https://pics.dmm.co.jp/mono/movie/adult/{temp}/{temp}pl.jpg'
        print(f'link = {link}')
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
        }
        # 随机休眠
        time.sleep(random.randint(6, 30) / 3)
        response = requests.get(link, headers=headers)
        response.raise_for_status()
        with open(f'{target_dir}/{bangou}.jpg', 'wb') as jpg:
            jpg.write(response.content)
        break


get_pic_by_bangou('300MAAN-341', 'd:')
