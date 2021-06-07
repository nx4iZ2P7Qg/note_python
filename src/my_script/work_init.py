# coding=utf-8
import pyautogui

pyautogui.PAUSE = 2

pyautogui.FAILSAFE = True

# 启动企业微信
pyautogui.hotkey('win', 'r')
pyautogui.write('C:/Program Files (x86)/WXWork/WXWork.exe')
pyautogui.press('enter')

# 启动微信
pyautogui.hotkey('win', 'r')
pyautogui.write('C:/Program Files (x86)/Tencent/WeChat/WeChat.exe')
pyautogui.press('enter')

# 启动 v2rayN
pyautogui.hotkey('win', 'r')
pyautogui.write('D:/sync/app/v2rayN-Core/v2rayN.exe')
pyautogui.press('enter')

i = pyautogui.getActiveWindow()
print(i.title)
