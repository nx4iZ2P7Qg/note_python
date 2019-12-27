import re


# https://blog.csdn.net/zhangxinrun/article/details/7526044
def get_width(o):
    """Return the screen column width for unicode ordinal o."""
    widths = [
        (126, 1), (159, 0), (687, 1), (710, 0), (711, 1),
        (727, 0), (733, 1), (879, 0), (1154, 1), (1161, 0),
        (4347, 1), (4447, 2), (7467, 1), (7521, 0), (8369, 1),
        (8426, 0), (9000, 1), (9002, 2), (11021, 1), (12350, 2),
        (12351, 1), (12438, 2), (12442, 0), (19893, 2), (19967, 1),
        (55203, 2), (63743, 1), (64106, 2), (65039, 1), (65059, 0),
        (65131, 2), (65279, 1), (65376, 2), (65500, 1), (65510, 2),
        (120831, 1), (262141, 2), (1114109, 1),
    ]
    if o == 0xe or o == 0xf:
        return 0
    for num, wid in widths:
        if o <= num:
            return wid
    return 1


def txt_format(file_path):
    with open(file_path, 'r', encoding='utf-8') as origin:
        lines = origin.readlines()

    # 首先统计出二维数组列数
    # 2个以上空格分割字段
    split_str = ' {2,}'
    # 待统计列数，不含最后一列
    cols_count = len(re.split(split_str, lines[0])) - 1
    # 定义字段二维数组
    width_arr = [[0 for i in range(len(lines))] for j in range(cols_count)]

    # 统计每行各字段值最大宽度，并放入二维数组
    for i in range(len(lines)):
        if lines[i] == '\n':
            continue
        cols = re.split(split_str, lines[i])
        for j in range(cols_count):
            col = cols[j]
            # 字体的宽度
            col_len = 0
            for char in col:
                col_len += get_width(ord(char))
            width_arr[j][i] = col_len

    # 统计各列最大宽度
    max_width_arr = []
    for array in width_arr:
        max_width_arr.append(max(array))
    print(f'max_width_arr = {max_width_arr}')

    # 计算各列起始点
    # 定义soft tab长度
    tab_len = 4
    # 第一列起点为0
    start_arr = [0]
    for i in range(len(max_width_arr)):
        for j in range(100):
            if start_arr[i] + max_width_arr[i] < j * tab_len:
                start_arr.append(j * tab_len)
                break
    print(f'start_arr = {start_arr}')

    # 将内容按start_arr填充到文件
    with open(f'{file_path}_format.txt', 'w', encoding='utf-8') as new:
        for i in range(len(lines)):
            if lines[i] == '\n':
                new.write(lines[i])
                continue
            cols = re.split(split_str, lines[i])
            for j in range(len(cols)):
                # 最后一列
                if j == len(cols) - 1:
                    new.write(cols[j])
                else:
                    # 补充空格
                    new.write(cols[j] + ' ' * (start_arr[j + 1] - start_arr[j] - width_arr[j][i]))


txt_format('d:/desktop/item.txt')
