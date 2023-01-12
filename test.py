""" 测试程序 """


import sys

if sys.version_info < (3, 10):
    raise RuntimeError('\033[31mPython版本低于3.10，无法运行测试程序！\033[0m')


from math import cos, pi
from random import randint
from tkinter import TclError, messagebox

import tkintertools


def colorful(ind: int = 0, color: list[str | None] = [None, '#F1F1F1']) -> None:
    """ 颜色变幻 """
    if not ind:
        color[0], color[1] = color[1], '#%06X' % randint(0, 1 << 24)  # 随机颜色
    color = tkintertools.color(color, ind)  # 渐变色
    color_ = tkintertools.color(color)  # 对比色
    canvas_doc.configure(bg=color)  # 更新画布背景色
    for widget in canvas_main._widget:  # 遍历主画布所有虚拟控件
        widget.color_fill[0], widget.color_text[0] = color, color_  # 更改控件外观参数
        widget.state()  # 立即更新控件外观
    root.after(20, colorful, 0 if ind >= 1 else ind+0.01)  # 迭代执行函数


def draw(ind: int = 0, n: int = 100) -> None:
    """ 绘制球体 """
    canvas_graph.create_oval(
        canvas_graph.rate_x*(300-ind/3),  # 椭圆左上角横坐标
        canvas_graph.rate_y*(100-ind/3),  # 椭圆左上角纵坐标
        canvas_graph.rate_x*(400+ind),  # 椭圆右下角横坐标
        canvas_graph.rate_y*(200+ind),  # 椭圆右下角纵坐标
        fill='' if ind else 'white',  # 中心椭圆填充白色，其他透明
        outline=tkintertools.color(
            ('#000000', '#FFFFFF'), cos(ind*pi/2/n)),  # 渐变色
        width=4  # 宽度为 4
    )
    if ind < n:  # 终止条件
        root.after(20, draw, ind+1)  # 迭代执行函数


def update(ind: int = 0) -> None:
    """ 进度条更新 """
    bar.load(ind)  # 更新进度条
    if ind < 1:  # 终止条件
        root.after(1, update, ind+0.0001)  # 迭代执行函数


def shutdown() -> None:
    """ 关闭询问 """
    if messagebox.askyesno('测试程序', '是否退出测试程序?'):  # 询问弹窗
        root.quit()  # 退出测试程序


root = tkintertools.Tk('测试程序', '960x540', shutdown)
# root.minsize(960, 540)


canvas_main = tkintertools.Canvas(root, 960, 540)
canvas_main.place(x=0, y=0)
canvas_doc = tkintertools.Canvas(root, 960, 540)
canvas_doc.place(x=-960, y=0)
canvas_graph = tkintertools.Canvas(root, 960, 540)
canvas_graph.place(x=960, y=0)


tkintertools.CanvasButton(
    canvas_main, 10, 500, 120, 30, 0, '模块文档',
    command=lambda: (tkintertools.move(root, canvas_main, 960*canvas_main.rate_x, 0, 300, 'rebound'),
                     tkintertools.move(root, canvas_doc, 960*canvas_doc.rate_x, 0, 300, 'rebound')))
tkintertools.CanvasButton(
    canvas_main, 830, 500, 120, 30, 0, '图像测试',
    command=lambda: (tkintertools.move(root, canvas_main, -960*canvas_main.rate_x, 0, 300, 'rebound'),
                     tkintertools.move(root, canvas_graph, -960*canvas_graph.rate_x, 0, 300, 'rebound')))
tkintertools.CanvasButton(
    canvas_doc, 830, 500, 120, 30, 0, '返回主页',
    command=lambda: (tkintertools.move(root, canvas_main, -960*canvas_main.rate_x, 0, 300, 'rebound'),
                     tkintertools.move(root, canvas_doc, -960*canvas_doc.rate_x, 0, 300, 'rebound')))
tkintertools.CanvasButton(
    canvas_graph, 10, 500, 120, 30, 0, '返回主页',
    command=lambda: (tkintertools.move(root, canvas_main, 960*canvas_main.rate_x, 0, 300, 'rebound'),
                     tkintertools.move(root, canvas_graph, 960*canvas_graph.rate_x, 0, 300, 'rebound')))

tkintertools.CanvasText(
    canvas_main, 10, 10, 465, 200, 10, ('居中圆角文本框', '竖线光标'), justify='center')
tkintertools.CanvasText(
    canvas_main, 485, 10, 465, 200, 0, ('靠右方角文本框', '下划线光标'), cursor=' _')
tkintertools.CanvasEntry(
    canvas_main, 10, 220, 200, 25, 6, ('居中圆角输入框', '点击输入'), justify='center')
tkintertools.CanvasEntry(
    canvas_main, 750, 220, 200, 25, 0, ('靠右方角输入框', '点击输入'), '•')

tkintertools.CanvasButton(
    canvas_main, 10, 250, 120, 25, 6, '圆角按钮',
    command=lambda: tkintertools.move(canvas_main, label_1, 0, -120 * canvas_main.rate_y, 300, 'flat'))
tkintertools.CanvasButton(
    canvas_main, 830, 250, 120, 25, 0, '方角按钮',
    command=lambda: tkintertools.move(canvas_main, label_2, 0, -120 * canvas_main.rate_y, 300, 'smooth'))

label_1 = tkintertools.CanvasLabel(
    canvas_main, 225, 550, 250, 100, 10, '圆角标签\n移动模式:flat')
label_2 = tkintertools.CanvasLabel(
    canvas_main, 485, 550, 250, 100, 0, '方角标签\n移动模式:smooth')
button_1 = tkintertools.CanvasButton(
    canvas_doc, 830, 10, 120, 30, 0, '颜色变幻', command=lambda: (button_1.set_live(False), colorful()))
button_2 = tkintertools.CanvasButton(
    canvas_graph, 10, 10, 120, 30, 0, '绘制图形',  command=lambda: (button_2.set_live(False), draw()))

load = tkintertools.CanvasButton(
    canvas_main, 420, 250, 120, 25, 0, '加载进度', command=lambda: (update(), load.set_live(False)))
bar = tkintertools.ProcessBar(canvas_main, 220, 220, 520, 25)

canvas_doc.create_text(  # 模块说明文档
    15, 270, text=tkintertools.__doc__, font=('consolas', 12), anchor='w')

try:  # 加载图片
    canvas_graph.create_image(
        860, 100, image=tkintertools.PhotoImage('tkinter.png'))
except TclError:  # 缺少图片
    print('\033[31m缺少示例图片tkinter.png\033[0m')

root.mainloop()  # 消息事件循环
