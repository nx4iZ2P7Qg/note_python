# coding=utf-8
import pyautogui

# 每次 PyAutoGUI 调用后停顿
pyautogui.PAUSE = 0.1

pyautogui.FAILSAFE = True

# 鼠标位置
print(pyautogui.position())

# 鼠标移动并点击
pyautogui.click(x=90, y=2140)

# 输入
pyautogui.write('cal')

# 输入非字符
pyautogui.press('left')

# 组合键
pyautogui.hotkey('shift', '1')

# 右键
pyautogui.click(button='right')

# 滚轮
pyautogui.moveTo(2560, 1440)
pyautogui.scroll(-100)

# 横向滚轮
pyautogui.hscroll(100)

# 对话框
pyautogui.alert('alert')

# 截图
pyautogui.screenshot()
