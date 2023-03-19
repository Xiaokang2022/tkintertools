import tkintertools as tkt

root = tkt.Tk('ButtonTest', 500, 500)
canvas = tkt.Canvas(root, 500, 500)
canvas.place(x=0, y=0)


def colorful(x: int, y: int, width: int, height: int) -> None:
    """ 渐变色 """
    for i in range(width):
        color = tkt.color(('#FF0000', '#0000FF'), i/width)
        canvas.create_line(x+i, y, x+i, y+height, fill=color)


colorful(50, 280, 400, 100)

tkt.Button(canvas, 150, 135, 200, 50, 0, 'NormalButton')
tkt.Button(canvas, 100, 195, 300, 50, 10, 'RoundCornerButton')
tkt.Button(canvas, 150, 255, 200, 50, 0, 'DisableButton').set_live(False)
tkt.Button(canvas, 100, 315, 300, 50, 10,
           'TransparentButton', color_fill=tkt.COLOR_NONE)

tkt.SetProcessDpiAwareness()
root.mainloop()
