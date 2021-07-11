# coding=utf-8
import os
import re
import shutil


def batch_rename(dir_path):
    """
    批量文件重命名

    :param dir_path: 目标目录
    :return: 无
    """
    file_list = os.listdir(dir_path)
    i = 0
    for file in file_list:
        name_old_re = 'Guilty Crown 2011 EP(.*) \[BD 1920x1080 23.976fps AVC-yuv420p10 FLACx2\] - yan04000985&VCB-Studio.ass'
        re_obj = re.search(name_old_re, file)
        # name_new = f'[VCB-Studio] Saiki Kusuo no Sainan [{re_obj.group(1)}][Ma444-10p_1080p][x265_flac].sc.ass'
        name_new = f'Guilty Crown 2011 EP{re_obj.group(1)} [BD 1920x1080 23.976fps AVC-yuv420p10 FLACx2] - yan04000985&VCB-Studio.ass'
        shutil.copy(os.path.join(dir_path, file), os.path.join(dir_path, name_new))


batch_rename(r'\\10.0.0.70\vid\anime\ギルティクラウン\诸神字幕组')
