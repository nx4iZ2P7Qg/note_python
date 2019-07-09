# coding=utf-8

import re

import requests


def get_pic_by_bangou(bangou, target_dir='.'):
    """
    根据车牌号获取相应图片

    :param bangou: 车牌号
    :param target_dir: 目录
    :return: 正常返回ok，执行完成未拿到图片返回error，异常返回相应信息
    """
    bangou = bangou.upper()
    # 校验
    if '-' not in bangou:
        return 'not a bangou'
    split = bangou.split('-')
    if not split[0].isalnum():
        return 'not a bangou'
    if not split[1].isdigit():
        return 'not a bangou'
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
        bangou = bangou.lower()
        # 'https://image.mgstage.com/images      /luxutv               /259luxu   /1007/pb_e_259luxu-1007.jpg'
        # 'https://image.mgstage.com/images      /ara                  /261ara    /331 /pb_e_261ara-331.jpg'
        # 'https://image.mgstage.com/images      /prestigepremium      /300maan   /341 /pb_e_300maan-341.jpg'
        link = f'https://image.mgstage.com/images/{path_dict[split[0]]}/{split[0]}/{split[1]}/pb_e_{bangou}.jpg'
    else:
        temp = bangou.replace('-', '').lower()
        # 'https://pics.dmm.co.jp/mono/movie/adult/ipx232/ipx232pl.jpg'
        link = f'https://pics.dmm.co.jp/mono/movie/adult/{temp}/{temp}pl.jpg'
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }
    print(f'link 01 = {link}')
    # 随机休眠
    # time.sleep(random.randint(6, 30) / 3)
    response = requests.get(link, headers=headers)
    response.raise_for_status()
    # 图片超过50KB被认为是有效图片
    if len(response.content) > 50_000:
        with open(f'{target_dir}/{bangou}.jpg', 'wb') as jpg:
            jpg.write(response.content)
        return 'ok'
    # 少数图片以上地址缺少，比如WANZ-197，下面定义备用地址
    bus_link = f'https://www.javbus.com/{bangou}'
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
        with open(f'{target_dir}/{bangou}.jpg', 'wb') as jpg:
            jpg.write(response.content)
        return 'ok'
    return 'error'


print(get_pic_by_bangou('336KNB-054', 'd:'))
