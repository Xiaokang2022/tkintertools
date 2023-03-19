import tkintertools as tkt

root = tkt.Tk('ColorTest', 500, 500)
canvas = tkt.Canvas(root, 500, 500)
canvas.place(x=0, y=0)


def colorful(x: int, y: int, width: int, height: int) -> None:
    """ 渐变色 """
    for i in range(width):
        color = tkt.color(('#FF0000', '#00FF00'), i/width)
        color_2 = tkt.color(('#FFFFFF', '#000000'), i/width)
        canvas.create_line(x+i, y, x+i, y+height, fill=color)
        canvas.create_oval(250-i/3, 300-i/3, 250+i/3, 300 +
                           i/3, outline=color_2, width=2)


colorful(50, 50, 400, 100)

tkt.SetProcessDpiAwareness()
root.mainloop()
