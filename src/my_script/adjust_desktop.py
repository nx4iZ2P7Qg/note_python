import pyautogui


def adjust_desktop():
    """
    调整桌面各窗口位置及大小

    家，32寸，4k屏幕，150%缩放
    """
    for win in pyautogui.getAllWindows():
        print(win)
        screen_width = 3840
        task_bar_height = 50
        screen_height = 2160 - task_bar_height
        middle_width = screen_width / 2
        middle_height = screen_height / 2

        if '- Firefox Developer Edition' in win.title:
            win.left = 80
            win.top = 0
            win.width = middle_width - win.left - 20
            win.height = middle_height
        elif '- Chromium' in win.title:
            win.left = middle_width
            win.top = 0
            win.width = middle_width
            win.height = middle_height
        # 文件浏览器，this pc页面
        elif 'This PC' in win.title:
            win.left = 80
            win.top = middle_height
            win.width = middle_width - 200
            win.height = middle_height - 120
        elif 'Netease Music' in win.title:
            win.left = middle_width
            win.top = middle_height
            win.width = middle_width
            win.height = middle_height
        elif '- PyCharm' in win.title:
            win.left = 0
            win.top = middle_height - 300
            win.width = middle_width
            win.height = middle_height + 300
        elif '- Visual Studio Code' in win.title:
            win.left = middle_width
            win.top = middle_height
            win.width = middle_width
            win.height = middle_height
        # 没连接终端时调整，调整后要重启
        elif 'MobaXterm' in win.title:
            win.left = middle_width
            win.top = middle_height
            win.width = middle_width
            win.height = middle_height
        elif 'Volume Mixer -' in win.title:
            win.left = 2582
            win.top = 1648
            win.width = 1258
            win.height = 462
        elif '- Remote Desktop Connection' in win.title:
            win.left = 0
            win.top = middle_height - 66
        elif '[foobar2000' in win.title:
            win.left = middle_width
            win.top = middle_height
            win.width = middle_width
            win.height = middle_height


adjust_desktop()
