# coding = utf-8
import os
import re
import shutil

PATH_BACK_UP_ROOT_DESKTOP = 'z:/back_up/desktop/'

# ============================== 软件配置 ==============================
# filezilla 配置
PATH_FILEZILLA = "C:/Users/DF/AppData/Roaming/FileZilla/"
# obs配置
PATH_OBS = 'C:/Users/DF/AppData/Roaming/obs-studio/basic/profiles/'
# thunderbird
PATH_THUNDER_BIRD = 'C:/Users/DF/AppData/Roaming/Thunderbird/Profiles/'
# firefox developer edition
PATH_FIREFOX_DEVELOPER = 'C:/Users/DF/AppData/Roaming/Mozilla/Firefox/Profiles/'
# chrome
# idea
# intellij idea
# intellij idea community edition
# intellij pycharm community edition
# postman请求
# postgres
# visual studio code
PATH_VISUAL_STUDIO_CODE = 'C:/Users/DF/AppData/Roaming/Code'

# tampermonkey
# Google Hit Hider by Domain 域名列表

# 常驻 game 数据

# ============================== 模拟器 ==============================
# dolphin
PATH_DOLPHIN_CONFIG = 'C:/Users/DF/Documents/Dolphin Emulator/Config/'
PATH_DOLPHIN_SCREENSHOTS = 'C:/Users/DF/Documents/Dolphin Emulator/ScreenShots/'

# ============================== 工作文档 ==============================
# 手动备份内容
PATH_WORK_DOCUMENT = 'D:/backup/'

back_up_tuple_desktop = {
    PATH_FILEZILLA,
    PATH_OBS,

    PATH_DOLPHIN_CONFIG,
    PATH_DOLPHIN_SCREENSHOTS,
}

back_up_tuple_laptop = {
    PATH_FILEZILLA,
    PATH_THUNDER_BIRD,
    PATH_FIREFOX_DEVELOPER,

    PATH_WORK_DOCUMENT,
}

choice = input("please choose back_up_tuple\n1==desktop\n2==laptop")
back_up_tuple = None
if choice == 1:
    back_up_tuple = back_up_tuple_desktop
elif choice == 2:
    back_up_tuple = back_up_tuple_laptop

for path_src in back_up_tuple:
    if not os.path.exists(path_src):
        print(f'not exist continue {path_src}')
        continue
    # print(path_src)
    # 寻找路径中的c: 转换成c__
    match = re.search('[C-Z]:', path_src)
    # c: -> __c__
    path_dst = f'{PATH_BACK_UP_ROOT_DESKTOP}{path_src}'.replace(match[0], f'__{match[0][0]}__', 1)
    if os.path.exists(path_dst):
        print(f'exist continue {path_dst}')
        continue
    shutil.copytree(path_src, path_dst)
