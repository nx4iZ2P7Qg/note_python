import pyautogui


def adjust_desktop():
    """
    调整桌面各窗口位置及大小

    办公室，27寸，4k屏幕，125%缩放
    """
    for win in pyautogui.getAllWindows():
        print(f'title={win.title}, left={win.left}, top={win.top}, width={win.width}, height={win.height}')
        screen_width = 3840
        task_bar_height = 50
        screen_height = 2160 - task_bar_height
        middle_width = screen_width / 2
        middle_height = screen_height / 2

        # 全屏
        if '- Mozilla Thunderbird' in win.title:
            win.maximize()
        # 左上
        elif 'Firefox Developer Edition' in win.title:
            win.left = 80
            win.top = 0
            win.width = middle_width - win.left
            win.height = middle_height
        # 左下
        elif ' PyCharm' in win.title or '- PyCharm' in win.title:
            win.left = 0
            win.top = middle_height
            win.width = middle_width
            win.height = middle_height
        # 右上
        elif '- Oracle VM VirtualBox' in win.title:
            win.left = middle_width
            win.top = 0
            win.width = middle_width
            win.height = middle_height
        # 右下
        elif '- Visual Studio Code' in win.title or \
                '- KiTTY' in win.title or \
                '[foobar2000' in win.title:
            win.left = middle_width
            win.top = middle_height
            win.width = middle_width
            win.height = middle_height
        # 没连接终端时调整，调整后要重启
        # elif 'MobaXterm' in win.title:
        #     win.maximize()
        # 音量合成器
        elif 'Volume Mixer -' in win.title:
            win.left = 2582
            win.top = 1548
            win.width = 1258
            win.height = 462
        # 左下，文件浏览器
        elif '此电脑' in win.title or 'This PC' in win.title:
            win.left = 80
            win.top = middle_height
            win.width = middle_width - 200
            win.height = middle_height - 120
        # 左下，远程连接
        elif '- Remote Desktop Connection' in win.title:
            win.left = 0
            win.top = middle_height - 66
        # im
        elif 'WeChat Work' in win.title or \
                '企业微信' in win.title or \
                '微信' in win.title or \
                'TIM' in win.title:
            win.left = 700
            win.top = 1100
            # win.width = 690
            # win.height = 718
        # edge
        elif '- Microsoft​ Edge' in win.title:
            win.left = middle_width
            win.top = 1900
            win.width = middle_width
            win.height = 200


adjust_desktop()
