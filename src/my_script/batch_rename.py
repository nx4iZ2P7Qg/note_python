# coding=utf-8
import os


def batch_rename(dir_path):
    """
    批量文件重命名

    :param dir_path: 目标目录
    :return: 无
    """
    file_list = os.listdir(dir_path)
    i = 0
    for file in file_list:
        i = i + 1
        # 使用001，002……命名
        new_file_name = str(i).zfill(3)
        # 保留扩展名
        file_extension = file[file.rindex('.'):]
        os.rename(dir_path + '/' + file, dir_path + '/' + new_file_name + file_extension)


batch_rename('d:/download/new folder/')
