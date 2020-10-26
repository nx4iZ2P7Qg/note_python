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
    line_count = len(lines)

    # 2个以上空格，一个或多个制表
    split_str = ' {2,}|\t+'

    # 各行各列宽度
    txt_width_arr = []
    # 各列最大宽度
    col_max_len_map = {}
    for i in range(line_count):
        lines[i] = lines[i].strip()
        line_arr = re.split(split_str, lines[i])
        txt_width = {}
        for j in range(len(line_arr)):
            col = line_arr[j]
            # 字体的宽度
            col_len = 0
            for char in col:
                col_len += get_width(ord(char))
            txt_width[j] = col_len
            if j in col_max_len_map:
                if col_max_len_map[j] <= col_len:
                    col_max_len_map[j] = col_len
            else:
                col_max_len_map[j] = col_len
        txt_width_arr.append(txt_width)

    # 计算各列起始点为 tab 的倍数
    tab_len = 4
    col_location_map = {}
    for k in col_max_len_map:
        v = col_max_len_map[k]
        # 防止字段间只隔1个空格引起歧义
        if v % tab_len == tab_len - 1:
            col_location_map[k] = v + 1 + tab_len
        else:
            col_location_map[k] = v + (tab_len - v % tab_len)

    # 填充行
    with open(f'{file_path}_format.txt', 'w', encoding='utf-8') as new:
        for i in range(line_count):
            line_arr = re.split(split_str, lines[i])
            for j in range(len(line_arr)):
                if j != 0:
                    new.write(' ' * (col_location_map[j - 1] - txt_width_arr[i][j - 1]))
                new.write(line_arr[j])
            new.write('\n')


txt_format('D:\\tmp.txt')
