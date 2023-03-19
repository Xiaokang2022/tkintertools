""" 测试程序 """

import sys

if sys.version_info < (3, 10):
    error_info = '\n\033[31mOperation Requirements: \033[32m\nPython version shall not be less than\033[33m 3.10.0!\033[0m'
    raise RuntimeError(error_info)

from math import cos, pi
from random import randint
from tkinter import Menu, TclError, messagebox
from winsound import Beep

import tkintertools as tkt


def colorful(ind: int = 0, color: list[str | None] = [None, '#F1F1F1']) -> None:
    """ 颜色变幻 """
    if not ind:
        color[0], color[1] = color[1], '#%06X' % randint(0, 1 << 24)  # 随机颜色
    color = tkt.color(color, ind)  # 渐变色
    color_ = tkt.color(color)  # 对比色
    canvas_doc.configure(bg=color)  # 更新画布背景色
    for widget in canvas_main._widget:  # 遍历主画布所有虚拟控件
        widget.color_fill[0], widget.color_text[0] = color, color_  # 更改控件外观参数
        widget.state()  # 立即更新控件外观
    root.after(20, colorful, 0 if ind >= 1 else ind+0.01)  # 迭代执行函数


def draw(ind: int = 0, n: int = 200) -> None:
    """ 绘制球体 """
    canvas_graph.create_oval(
        canvas_graph.rx*(500-ind/3),  # 椭圆左上角横坐标
        canvas_graph.ry*(300-ind/3),  # 椭圆左上角纵坐标
        canvas_graph.rx*(600+ind),  # 椭圆右下角横坐标
        canvas_graph.ry*(400+ind),  # 椭圆右下角纵坐标
        fill='' if ind else 'white',  # 中心椭圆填充白色，其他透明
        outline=tkt.color(('#000000', '#FFFFFF'), cos(ind*pi/2/n)),  # 渐变色
        width=3)
    if ind < n:  # 终止条件
        root.after(10, draw, ind+1)  # 迭代执行函数


def update(ind: int = 0) -> None:
    """ 进度条更新 """
    bar.load(ind)  # 更新进度条
    if ind < 1:  # 终止条件
        root.after(1, update, ind+0.0002)  # 迭代执行函数


def shutdown() -> None:
    """ 关闭询问 """
    if messagebox.askyesno('测试程序', '是否退出测试程序?'):  # 询问弹窗
        root.quit()  # 退出测试程序


root = tkt.Tk('tkintertools', 1280, 720, shutdown=shutdown)
root.minsize(640, 360)
menu = Menu(root, tearoff=False)
root.configure(menu=menu)
canvas_main = tkt.Canvas(root, 1280, 720)
canvas_main.place(x=0, y=0)
canvas_doc = tkt.Canvas(root, 1280, 720)
canvas_doc.place(x=-1280, y=0)
canvas_graph = tkt.Canvas(root, 1280, 720)
canvas_graph.place(x=1280, y=0)


def sound(): return Beep(600, 100)


tkt.Button(
    canvas_main, 10, 660, 200, 50, 0, '模块文档',
    command=lambda: (tkt.move(root, canvas_main, 1280*canvas_main.rx, 0, 500, 'rebound'),
                     tkt.move(root, canvas_doc, 1280*canvas_doc.rx, 0, 500, 'rebound'))
).command_ex['press'] = sound
tkt.Button(
    canvas_main, 1070, 660, 200, 50, 0, '图像测试',
    command=lambda: (tkt.move(root, canvas_main, -1280*canvas_main.rx, 0, 500, 'rebound'),
                     tkt.move(root, canvas_graph, -1280*canvas_graph.rx, 0, 500, 'rebound'))
).command_ex['press'] = sound
tkt.Button(
    canvas_doc, 1070, 660, 200, 50, 0, '返回主页',
    command=lambda: (tkt.move(root, canvas_main, -1280*canvas_main.rx, 0, 500, 'rebound'),
                     tkt.move(root, canvas_doc, -1280*canvas_doc.rx, 0, 500, 'rebound'))
).command_ex['press'] = sound
tkt.Button(
    canvas_graph, 10, 660, 200, 50, 0, '返回主页',
    command=lambda: (tkt.move(root, canvas_main, 1280*canvas_main.rx, 0, 500, 'rebound'),
                     tkt.move(root, canvas_graph, 1280*canvas_graph.rx, 0, 500, 'rebound'))
).command_ex['press'] = sound

tkt.Text(
    canvas_main, 10, 10, 625, 300, 20, ('居中圆角文本框', '竖线光标'), justify='center')
tkt.Text(
    canvas_main, 645, 10, 625, 300, 0, ('靠右方角文本框', '下划线光标'), cursor=' _')
tkt.Entry(
    canvas_main, 10, 320, 300, 35, 10, ('居中圆角输入框', '点击输入'), justify='center')
tkt.Entry(
    canvas_main, 970, 320, 300, 35, 0, ('靠右方角输入框', '点击输入'), '•')

tkt.Button(
    canvas_main, 10, 365, 200, 40, 10, '圆角按钮',
    command=lambda: tkt.move(
        canvas_main, label_1, 0, -170 * canvas_main.ry, 500, 'flat')
).command_ex['press'] = sound
tkt.Button(
    canvas_main, 1070, 365, 200, 40, 0, '方角按钮',
    command=lambda: tkt.move(
        canvas_main, label_2, 0, -170 * canvas_main.ry, 500, 'smooth')
).command_ex['press'] = sound

label_1 = tkt.Label(
    canvas_main, 235, 730, 400, 150, 20, '圆角标签\n移动模式:flat')
label_2 = tkt.Label(
    canvas_main, 645, 730, 400, 150, 0, '方角标签\n移动模式:smooth')
button_1 = tkt.Button(
    canvas_doc, 1070, 10, 200, 50, 0, '颜色变幻', command=lambda: (button_1.set_live(False), colorful()))
button_1.command_ex['press'] = sound
button_2 = tkt.Button(
    canvas_graph, 10, 10, 200, 50, 0, '绘制图形',  command=lambda: (button_2.set_live(False), draw()))
button_2.command_ex['press'] = sound

load = tkt.Button(
    canvas_main, 540, 365, 200, 40, 0, '加载进度', command=lambda: (update(), load.set_live(False)))
load.command_ex['press'] = sound
bar = tkt.Progressbar(canvas_main, 320, 320, 640, 35)

canvas_doc.create_text(  # 模块说明文档
    15, 360, text=tkt.__doc__, font=('consolas', 16, 'italic'), anchor='w')

try:  # 加载图片
    canvas_graph.create_image(
        1150, 130, image=tkt.PhotoImage('tkintertools.png'))
except TclError:  # 缺少图片
    print('\033[31m缺少示例图片tkinter.png\033[0m')

tkt.SetProcessDpiAwareness()  # 设置DPI级别
root.mainloop()  # 消息事件循环
