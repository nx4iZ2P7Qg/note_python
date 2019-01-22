# 当前流行的图形编程包: PyGtk PyQt TkInter wxPython
from tkinter import *


# 按键事件
def print_hello():
    t.insert('1.0', "hello\n")


# 主窗口
window = Tk()
window.title("GUI demo")
window.geometry('1280x720')
window.resizable(width=False, height=True)

# 文本框
t = Text()
t.pack()

# 按钮
Button(window, text="press", command=print_hello).pack()

# 消息循环
window.mainloop()
