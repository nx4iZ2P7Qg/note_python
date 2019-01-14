import os

# 系统名，window10是nt，CentOS7是posix
print(os.name)

# 通用路径/home/dexter/aria2
# win平台也可以使用，会自动把驱动器加在前面，具体是哪个驱动器，似乎取决于运行python文件的驱动器
path = os.path.join(os.path.sep, 'home', 'dexter', 'aria2')
# windows平台路径包含驱动器的路径
os.path.abspath(path)

# 文件及目录操作
os.listdir('directory')
os.rename('old.txt', 'new.txt')
os.remove("app1.log")
os.getcwd()
os.chdir('d:')
os.mkdir('d:/python_test_dir', 777)
os.rmdir('d:/python_test_dir')

# 遍历
for root, dirs, files in os.walk(r'C:\Users\DF\Desktop\corejava9'):
    print(f'root = {root}, dirs = {dirs}, files = {files}')
