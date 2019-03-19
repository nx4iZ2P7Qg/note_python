# coding = utf-8
import os
import re
import shutil

PATH_BACK_UP_ROOT_DESKTOP = 'z:/back_up/desktop/'

# ============================== 软件配置 ==============================

# filezilla 配置
PATH_FILEZILLA = "C:/Users/DF/AppData/Roaming/FileZilla/"

# obs配置
PATH_OBS = 'C:/Users/DF/AppData/Roaming/obs-studio/basic/profiles/Untitled/'

# thunderbird

# firefox developer edition

# chrome

# idea

# intellij idea

# intellij idea community edition

# intellij pycharm community edition

# postman请求


# ============================== 游戏 ==============================

# 夏娃年代记 哈尼喵汉化组
PATH_EVENICLE = 'C:/Users/DF/Documents/AliceSoft/夏娃年代记汉化版V1.00【哈尼喵汉化组】 此汉化免费发布，若是花了钱，请去退货退款给差评/'

# FF12 CPY
PATH_FFXII = 'C:/Users/DF/Documents/My Games/FINAL FANTASY XII THE ZODIAC AGE/'

# 上古卷轴5 天际
PATH_THE_ELDER_SCROLLS_V_SKYRIM = 'C:/Users/DF/Documents/My Games/Skyrim Special Edition/'

# FFVIII STEAM FLT
PATH_FFVIII = 'C:/Users/DF/Documents/Square Enix/FINAL FANTASY VIII Steam/'

# 生化危机4 终极高清版 3DM
PATH_RE4 = 'C:/ProgramData/Steam/3DMGAME/254700/'

# 怪物猎人世界 CODEX
PATH_MHW = 'C:/Users/Public/Documents/Steam/CODEX/582010/'

# 生化危机2 重制版 CODEX
PATH_RE2_RE = 'C:/Users/Public/Documents/Steam/CODEX/883710/'

# vr女友 DARKSIDERS
PATH_VR_KANOJO = 'D:/games/VR Kanojo/UserData/'

# honey select zod
PATH_HONEY_SELECT = 'D:/games/HoneySelect/UserData/'

# dolphin
PATH_DOLPHIN_CONFIG = 'C:/Users/DF/Documents/Dolphin Emulator/Config/'
PATH_DOLPHIN_SCREENSHOTS = 'C:/Users/DF/Documents/Dolphin Emulator/ScreenShots/'

back_up_tuple = {
    PATH_FILEZILLA,
    PATH_OBS,

    PATH_EVENICLE,
    PATH_FFXII,
    PATH_THE_ELDER_SCROLLS_V_SKYRIM,
    PATH_FFVIII,
    PATH_RE4,
    PATH_MHW,
    PATH_RE2_RE,
    PATH_VR_KANOJO,
    PATH_HONEY_SELECT,

    PATH_DOLPHIN_CONFIG,
    PATH_DOLPHIN_SCREENSHOTS,
}

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

