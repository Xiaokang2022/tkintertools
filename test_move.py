import tkintertools as tkt

root = tkt.Tk('MoveTest', 500, 500)
canvas = tkt.Canvas(root, 500, 500)
canvas.place(x=0, y=0)

rect = canvas.create_rectangle(50, 350, 150, 450)


def move_window(switch: list[bool] = [True]) -> None:
    """ 移动窗口 """
    tkt.move(root, None, 1000 if switch[0] else -1000, 0, 800, 'flat')
    switch[0] = not switch[0]


def move_button(switch: list[bool] = [True]) -> None:
    """ 移动按钮 """
    tkt.move(canvas, button, 200 if switch[0] else -200, 0, 500, 'rebound')
    switch[0] = not switch[0]


def move_rect(switch: list[bool] = [True]) -> None:
    """ 移动画布绘制的矩形 """
    tkt.move(canvas, rect, 200 if switch[0] else -200, 0, 500, 'smooth')
    switch[0] = not switch[0]


tkt.Button(canvas, 50, 50, 200, 40, 10, 'MoveWindow', command=move_window)
tkt.Button(canvas, 50, 100, 200, 40, 10, 'MoveRect', command=move_rect)
button = tkt.Button(canvas, 50, 150, 200, 40, 10,
                    'MoveButton', command=move_button)


tkt.SetProcessDpiAwareness()
root.mainloop()
