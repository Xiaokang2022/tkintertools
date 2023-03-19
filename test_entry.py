import tkintertools as tkt

root = tkt.Tk('EntryTest', 500, 400)
canvas = tkt.Canvas(root, 500, 400)
canvas.place(x=0, y=0)


def colorful(x: int, y: int, width: int, height: int) -> None:
    """ 渐变色 """
    for i in range(width):
        color = tkt.color(('#FF0000', '#0000FF'), i/width)
        canvas.create_line(x+i, y, x+i, y+height, fill=color)


colorful(50, 193, 400, 100)
tkt.Entry(canvas, 20, 20, 200, 30, 0, ('LeftEntry', 'Enter'))
tkt.Entry(canvas, 20, 55, 200, 30, 0,
          ('CenterEntry', 'Enter'), justify='center')
tkt.Entry(canvas, 20, 90, 200, 30, 0, ('RightEntry', 'Enter'), justify='right')
tkt.Entry(canvas, 270, 20, 200, 30, 8, 'LeftEntry')
tkt.Entry(canvas, 270, 55, 200, 30, 8, 'CenterEntry', justify='center')
tkt.Entry(canvas, 270, 90, 200, 30, 8, 'RightEntry', justify='right')

tkt.Entry(canvas, 100, 150, 300, 35, 0,
          ('PasswordEntry', 'Click To Enter'), justify='center', show='•')
tkt.Entry(canvas, 100, 200, 300, 35, 0, 'DisableEntry',
          justify='center').set_live(False)
tkt.Entry(canvas, 100, 250, 300, 35, 0, 'TransparentEntry',
          justify='center', color_fill=tkt.COLOR_NONE)

tkt.SetProcessDpiAwareness()
root.mainloop()
