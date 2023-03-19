import tkintertools as tkt

root = tkt.Tk('TextTest', 1000, 400)
canvas = tkt.Canvas(root, 1000, 400)
canvas.place(x=0, y=0)


def colorful(x: int, y: int, width: int, height: int) -> None:
    """ 渐变色 """
    for i in range(width):
        color = tkt.color(('#FF0000', '#0000FF'), i/width)
        canvas.create_line(x+i, y, x+i, y+height, fill=color)


colorful(510, 175, 480, 150)

tkt.Text(canvas, 50, 50, 400, 100, 0, ('NormalText(Left)', 'Click To Enter'))
tkt.Text(canvas, 50, 200, 400, 100, 20,
         'RoundCornerText(Center)', justify='center')
tkt.Text(canvas, 550, 50, 400, 100, 0, 'DisableText').set_live(False)
tkt.Text(canvas, 550, 200, 400, 100, 20,
         'TransparentText(Right)', justify='right', color_fill=tkt.COLOR_NONE)

tkt.SetProcessDpiAwareness()
root.mainloop()
