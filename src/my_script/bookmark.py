def transform(path_old, path_new):
    """
    将 firefox 导出的 bookmark，按目录添加 tag

    :param path_old: 源文件
    :param path_new: 新文件
    :return: None
    """
    with open(path_old, 'r', encoding='utf-8') as bookmark:
        # 标签列表，文件夹 a 中的文件夹 b，会表示为 ['a', 'b']
        tag_arr = []
        # 应该使用的 tag 索引
        index = -1
        with open(path_new, 'w', encoding='utf-8') as new:
            for line in bookmark.readlines():
                i = line.find('<H3 ')
                if i != -1:
                    j = line.find('>', i)
                    k = line.find('</H3')
                    fold = line[j + 1: k].replace(' ', '')

                    try:
                        tag_arr[index] = fold
                    except Exception as e:
                        tag_arr.append(fold)

                i = line.find('<DL><p>')
                if i != -1:
                    index = index + 1

                i = line.find('<DT><A ')
                if i != -1:
                    j = line.find('ADD_DATE=')
                    if j == -1:
                        print('缺少 ADD_DATE=\n' + line)
                        exit(-1)
                    else:
                        if index == -1:
                            new_line = f'{line[:j]}TAGS="notag" {line[j:]}'
                        else:
                            new_line = f'{line[:j]}TAGS="{",".join(tag_arr[:index])}" {line[j:]}'
                        new.write(new_line)
                        continue

                i = line.find('</DL><p>')
                if i != -1:
                    index = index - 1
                    if index == -1:
                        tag_arr = []

                new.write(line)


transform('d:\\bookmarks.html', 'd:\\bookmarks_new.html')
