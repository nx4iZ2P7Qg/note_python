# coding=utf-8
import pyautogui
import time


def sleep():
    time.sleep(1.0)


pyautogui.PAUSE = 0.5

pyautogui.FAILSAFE = True

# 启动企业微信
pyautogui.hotkey('win', 's')

sleep()

pyautogui.write('wxwork')

pyautogui.press('enter')

# 启动微信
pyautogui.hotkey('win', 's')

sleep()

pyautogui.write('we')

pyautogui.press('enter')

# 启动tim
pyautogui.hotkey('win', 's')

sleep()

pyautogui.write('tim')

pyautogui.press('enter')

# 启动tim
pyautogui.hotkey('win', 's')

sleep()

pyautogui.write('tim')

pyautogui.press('enter')

# 启动 trojan
pyautogui.hotkey('win', 's')

sleep()

pyautogui.write('trojan')

pyautogui.press('enter')

# 启动 firefox
# pyautogui.hotkey('win', 's')
#
# sleep()
#
# pyautogui.write('firefox develop')
#
# pyautogui.press('enter')


i = pyautogui.getActiveWindow()
print(i.title)
