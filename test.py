""" Test program """

from math import cos, pi
from random import randint
from tkinter import TclError, messagebox

import tkintertools as tkt


def colorful(
    ind=0,  # type: int
    color=[None, '#F1F1F1']  # type: list[str | None]
):  # type: (...) -> None
    """ Change color randomly and Gradiently """
    if not ind:
        color[0], color[1] = color[1], '#%06X' % randint(0, 1 << 24)
    color = tkt.color(color, ind)
    color_ = tkt.color(color)
    canvas_doc.configure(bg=color)
    for widget in canvas_main._widget:
        widget.color_fill[0], widget.color_text[0] = color, color_
        widget.state()
    root.after(20, colorful, 0 if ind >= 1 else ind+0.01)


def draw(ind=0, n=200):  # type: (int, int) -> None
    """ Draw a sphere """
    canvas_graph.create_oval(
        canvas_graph.rx*(500-ind/3),
        canvas_graph.ry*(300-ind/3),
        canvas_graph.rx*(600+ind),
        canvas_graph.ry*(400+ind),
        fill='' if ind else 'white',
        outline=tkt.color(('#000000', '#FFFFFF'), cos(ind*pi/2/n)), width=3)
    if ind < n:
        root.after(10, draw, ind+1)


def update(ind=0):  # type: (int) -> None
    """ Load the progress """
    bar.load(ind)
    if ind < 1:
        root.after(2, update, ind+0.0002)


def shutdown():  # type: () -> None
    """ Ask before quit """
    if messagebox.askyesno('Test program', 'Do you want to exit the test program?'):
        root.quit()


root = tkt.Tk('tkintertools', 1280, 720, shutdown=shutdown)
root.minsize(640, 360)
canvas_main = tkt.Canvas(root, 1280, 720, 0, 0)
canvas_doc = tkt.Canvas(root, 1280, 720, -1280, 0)
canvas_graph = tkt.Canvas(root, 1280, 720, 1280, 0)


tkt.Button(
    canvas_main, 10, 660, 200, 50, text='Doc',
    command=lambda: (tkt.move(root, canvas_main, 1280*canvas_main.rx, 0, 500, mode='rebound'),
                     tkt.move(root, canvas_doc, 1280*canvas_doc.rx, 0, 500, mode='rebound')))
tkt.Button(
    canvas_main, 1070, 660, 200, 50, text='Image',
    command=lambda: (tkt.move(root, canvas_main, -1280*canvas_main.rx, 0, 500, mode='rebound'),
                     tkt.move(root, canvas_graph, -1280*canvas_graph.rx, 0, 500, mode='rebound')))
tkt.Button(
    canvas_doc, 1070, 660, 200, 50, text='Back',
    command=lambda: (tkt.move(root, canvas_main, -1280*canvas_main.rx, 0, 500, mode='rebound'),
                     tkt.move(root, canvas_doc, -1280*canvas_doc.rx, 0, 500, mode='rebound')))
tkt.Button(
    canvas_graph, 10, 660, 200, 50, text='Back',
    command=lambda: (tkt.move(root, canvas_main, 1280*canvas_main.rx, 0, 500, mode='rebound'),
                     tkt.move(root, canvas_graph, 1280*canvas_graph.rx, 0, 500, mode='rebound')))

tkt.Text(canvas_main, 10, 10, 625, 300, radius=20,
         text=('Centered and Rounded TextBox', 'Click to Input'), justify='center')
tkt.Text(canvas_main, 645, 10, 625, 300,
         text=('Right-leaning TextBox', 'Click to Input'), cursor=' _')
tkt.Entry(canvas_main, 10, 320, 300, 35, radius=10,
          text=('Rounded InputBox', 'Click to Input'), justify='center')
tkt.Entry(canvas_main, 970, 320, 300, 35, text=(
    'InputBox', 'Click to Input'), show='•')
tkt.Button(canvas_main, 10, 365, 300, 40, radius=10, text='Rounded Button', command=lambda: tkt.move(
    canvas_main, label_1, 0, -170 * canvas_main.ry, 500, mode='flat'))
tkt.Button(canvas_main, 1070, 365, 200, 40, text='Button', command=lambda: tkt.move(
    canvas_main, label_2, 0, -170 * canvas_main.ry, 500, mode='smooth'))
tkt.CheckButton(canvas_main, 10, 415, 35, radius=10,
                text='Rounded CheckButton')
tkt.CheckButton(canvas_main, 1235, 415, 35, value=True,
                text='CheckButton', justify='left')

label_1 = tkt.Label(canvas_main, 235, 730, 400, 150,
                    radius=20, text='Rounded Label\nmove mode: flat')
label_2 = tkt.Label(canvas_main, 645, 730, 400, 150,
                    text='Label\nmove mode: smooth')
button_1 = tkt.Button(canvas_doc, 1070, 10, 200, 50, text='Colorful',
                      command=lambda: (button_1.set_live(False), colorful()))
button_2 = tkt.Button(canvas_graph, 10, 10, 200, 50, text='Draw',
                      command=lambda: (button_2.set_live(False), draw()))

load = tkt.Button(canvas_main, 540, 365, 200, 40, text='Load',
                  command=lambda: (update(), load.set_live(False)))
bar = tkt.Progressbar(canvas_main, 320, 320, 640, 35)

font_chooseer = tkt.Button(canvas_main, 500, 465, 280, 40, text='Select a Font', command=lambda: tkt.askfont(
    root, lambda font: canvas_main.itemconfigure(font_chooseer.text, font=font)))

canvas_doc.create_text(
    15, 360, text=tkt.__doc__, font=(tkt.FONT, 14), anchor='w')

try:
    canvas_graph.create_image(
        1150, 130, image=tkt.PhotoImage('tkintertools.png'))
except TclError:
    print('\033[31mLoad tkintertools.png Error\033[0m')

root.mainloop()
