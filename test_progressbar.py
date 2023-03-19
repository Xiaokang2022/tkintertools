import tkintertools as tkt

root = tkt.Tk('ProgressbarTest', 500, 500)
canvas = tkt.Canvas(root, 500, 500)
canvas.place(x=0, y=0)


def colorful(x: int, y: int, width: int, height: int) -> None:
    """ 渐变色 """
    for i in range(width):
        color = tkt.color(('#FF0000', '#0000FF'), i/width)
        canvas.create_line(x+i, y, x+i, y+height, fill=color)


colorful(30, 290, 440, 50)

tkt.Progressbar(canvas, 50, 50, 400, 30)
tkt.Progressbar(canvas, 50, 100, 400, 30).load(.6667)
tkt.Progressbar(canvas, 50, 150, 400, 30, 5).load(1)
(_ := tkt.Progressbar(canvas, 50, 200, 400, 30)).load(0.3333)
_.set_live(False)
tkt.Progressbar(canvas, 50, 250, 400, 30, color_bar=(
    'lightyellow', 'skyblue')).load(.5)
tkt.Progressbar(canvas, 50, 300, 400, 30, color_bar=('', 'orange')).load(.1667)

progressbar = tkt.Progressbar(canvas, 50, 375, 400, 30)
progressbar_2 = tkt.Progressbar(canvas, 50, 425, 400, 30)


def load(total: int, count: int = 0) -> None:
    """ 进度条加载 """
    progressbar.load(count/total)
    progressbar_2.load(1-count/total)
    if count < total:
        root.after(3, load, total, count+1)


load(10000)

tkt.SetProcessDpiAwareness()
root.mainloop()
