# coding=utf-8
import pyautogui

# 每次 PyAutoGUI 调用后停顿
pyautogui.PAUSE = 1

# 鼠标在屏幕外且异常
pyautogui.FAILSAFE = True

# 屏幕长宽
screenWidth, screenHeight = pyautogui.size()

# 鼠标位置
currentMouseX, currentMouseY = pyautogui.position()

# 鼠标移动
pyautogui.moveTo(2560, 1440)
pyautogui.moveRel(100, 100)

# 鼠标点击
pyautogui.click()
pyautogui.click(x=100, y=200)
pyautogui.click('button.png')
pyautogui.click(button='right')
pyautogui.doubleClick()
pyautogui.click(button='left', clicks=10, interval=0.25)

# 输入
pyautogui.write('cal')

# 输入非字符
pyautogui.press('left')

# 键盘操作
pyautogui.keyDown('shift')
pyautogui.press('[left, left, left, left]')
pyautogui.keyUp('shift')

# 组合键
pyautogui.hotkey('shift', '1')

# 滚轮
pyautogui.scroll(-100)

# 横向滚轮
pyautogui.hscroll(100)

# 对话框
pyautogui.alert('alert')

# 截图
pyautogui.screenshot()
