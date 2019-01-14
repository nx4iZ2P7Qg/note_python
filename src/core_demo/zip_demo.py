import zipfile

# 解压
with zipfile.ZipFile(r'C:\Users\DF\Desktop\nas\vm-all-1.csar', 'r') as mano_csar:
    mano_csar.extractall(r'C:\Users\DF\Desktop\nas')

# 压缩
with zipfile.ZipFile(r'C:\Users\DF\Desktop\spring_mvc.zip', 'w', zipfile.ZIP_DEFLATED) as to_zip_file:
    to_zip_file.write(r'C:\Users\DF\Desktop\corejava9')
