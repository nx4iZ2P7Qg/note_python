import shutil

# 文件夹压缩
dir_name = r'C:\Users\DF\Desktop\corejava9'
shutil.make_archive('archive', 'zip', dir_name)

# 文件夹解压
shutil.unpack_archive('archive.zip', './java9', 'zip')
