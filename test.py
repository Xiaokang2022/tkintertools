""" Test program """

from math import cos, pi
from random import randint, sample
from tkinter import Event, TclError, messagebox

import tkintertools as tkt
from tkintertools import constants as cnt
from tkintertools import tools_3d as t3d


class Application:

    def __init__(self):
        self.root = tkt.Tk('tkintertools', 1280, 720, shutdown=self.shutdown)
        self.root.minsize(640, 360)
        self.canvas_main = tkt.Canvas(self.root, 1280, 720, 0, 0)
        self.canvas_doc = tkt.Canvas(self.root, 1280, 720, -1280, 0)
        self.canvas_graph = tkt.Canvas(self.root, 1280, 720, 1280, 0)
        self.canvas_3d = t3d.Canvas_3D(self.root, 1280, 720, 1280, 0)

        self.canvas_main_init()
        self.canvas_doc_init()
        self.canvas_graph_init()
        self.canvas_3d_init()

        self.root.bind('<Button-1>', lambda event: self.rotate(event, True))
        self.root.bind('<B1-Motion>', self.rotate)
        self.root.bind('<Button-3>', lambda event: self.translate(event, True))
        self.root.bind('<B3-Motion>', self.translate)
        self.root.bind('<MouseWheel>', self.scale)

        self.root.mainloop()

    def shutdown(self):  # type: () -> None
        """ Ask before quit """
        if messagebox.askyesno('Test program', 'Do you want to exit the test program?'):
            self.root.quit()

    def colorful(
        self,
        ind=0,  # type: int
        color=[None, '#F1F1F1']  # type: list[str | None]
    ):  # type: (...) -> None
        """ Change color randomly and Gradiently """
        if not ind:
            color[0], color[1] = color[1], '#%06X' % randint(0, 1 << 24)
        color = tkt.color(color, ind)
        color_ = tkt.color(color)
        self.canvas_doc.configure(bg=color)
        for widget in self.canvas_main._widget:
            widget.color_fill[0], widget.color_text[0] = color, color_
            widget.state()
        self.root.after(20, self.colorful, 0 if ind >= 1 else ind+0.01)

    def draw(self, ind=0, n=200):  # type: (int, int) -> None
        """ Draw a sphere """
        self.canvas_graph.create_oval(
            self.canvas_graph.rx*(500-ind/3),
            self.canvas_graph.ry*(300-ind/3),
            self.canvas_graph.rx*(600+ind),
            self.canvas_graph.ry*(400+ind),
            fill='' if ind else 'white',
            outline=tkt.color(('#000000', '#FFFFFF'), cos(ind*pi/2/n)), width=3)
        if ind < n:
            self.root.after(10, self.draw, ind+1)

    def update(self, ind=0):  # type: (int) -> None
        """ Load the progress """
        self.bar.load(ind)
        if ind < 1:
            self.root.after(2, self.update, ind+0.0002)

    def canvas_main_init(self):
        tkt.Button(
            self.canvas_main, 10, 660, 200, 50, text='Doc',
            command=lambda: (tkt.move(self.root, self.canvas_main, 1280*self.canvas_main.rx, 0, 500, mode='rebound'),
                             tkt.move(self.root, self.canvas_doc, 1280*self.canvas_doc.rx, 0, 500, mode='rebound')))
        tkt.Button(
            self.canvas_main, 1070, 660, 200, 50, text='Image',
            command=lambda: (tkt.move(self.root, self.canvas_main, -1280*self.canvas_main.rx, 0, 500, mode='rebound'),
                             tkt.move(self.root, self.canvas_graph, -1280*self.canvas_graph.rx, 0, 500, mode='rebound')))
        tkt.Text(self.canvas_main, 10, 10, 625, 300, radius=20,
                 text=('Centered and Rounded TextBox', 'Click to Input'), justify='center')
        tkt.Text(self.canvas_main, 645, 10, 625, 300,
                 text=('Right-leaning TextBox', 'Click to Input'), cursor=' _')
        tkt.Entry(self.canvas_main, 10, 320, 300, 35, radius=10,
                  text=('Rounded InputBox', 'Click to Input'), justify='center')
        tkt.Entry(self.canvas_main, 970, 320, 300, 35, text=(
            'InputBox', 'Click to Input'), show='•')
        tkt.Button(self.canvas_main, 10, 365, 300, 40, radius=10, text='Rounded Button', command=lambda: tkt.move(
            self.canvas_main, label_1, 0, -170 * self.canvas_main.ry, 500, mode='flat'))
        tkt.Button(self.canvas_main, 1070, 365, 200, 40, text='Button', command=lambda: tkt.move(
            self.canvas_main, label_2, 0, -170 * self.canvas_main.ry, 500, mode='smooth'))
        tkt.CheckButton(self.canvas_main, 10, 415, 35, radius=10,
                        text='Rounded CheckButton')
        tkt.CheckButton(self.canvas_main, 1235, 415, 35, value=True,
                        text='CheckButton', justify='left')
        label_1 = tkt.Label(self.canvas_main, 235, 730, 400, 150,
                            radius=20, text='Rounded Label\nmove mode: flat')
        label_2 = tkt.Label(self.canvas_main, 645, 730, 400, 150,
                            text='Label\nmove mode: smooth')
        load = tkt.Button(self.canvas_main, 540, 365, 200, 40, text='Load',
                          command=lambda: (self.update(), load.set_live(False)))
        self.bar = tkt.Progressbar(self.canvas_main, 320, 320, 640, 35)

        font_chooseer = tkt.Button(self.canvas_main, 500, 465, 280, 40, text='Select a Font', command=lambda: tkt.askfont(
            self.root, lambda font: self.canvas_main.itemconfigure(font_chooseer.text, font=font)))

    def canvas_doc_init(self):
        tkt.Button(
            self.canvas_doc, 1070, 660, 200, 50, text='Back',
            command=lambda: (tkt.move(self.root, self.canvas_main, -1280*self.canvas_main.rx, 0, 500, mode='rebound'),
                             tkt.move(self.root, self.canvas_doc, -1280*self.canvas_doc.rx, 0, 500, mode='rebound')))
        button_1 = tkt.Button(self.canvas_doc, 1070, 10, 200, 50, text='Colorful',
                              command=lambda: (button_1.set_live(False), self.colorful()))
        self.canvas_doc.create_text(
            15, 360, text=tkt.__doc__, font=(cnt.FONT, 14), anchor='w')

    def canvas_graph_init(self):
        tkt.Button(
            self.canvas_graph, 1070, 660, 200, 50, text='3D',
            command=lambda: (tkt.move(self.root, self.canvas_graph, -1280*self.canvas_main.rx, 0, 500, mode='rebound'),
                             tkt.move(self.root, self.canvas_3d, -1280*self.canvas_graph.rx, 0, 500, mode='rebound')))
        tkt.Button(
            self.canvas_graph, 10, 660, 200, 50, text='Back',
            command=lambda: (tkt.move(self.root, self.canvas_main, 1280*self.canvas_main.rx, 0, 500, mode='rebound'),
                             tkt.move(self.root, self.canvas_graph, 1280*self.canvas_graph.rx, 0, 500, mode='rebound')))
        button_2 = tkt.Button(self.canvas_graph, 10, 10, 200, 50, text='Draw',
                              command=lambda: (button_2.set_live(False), self.draw()))
        try:
            self.canvas_graph.create_image(
                1150, 130, image=tkt.PhotoImage('tkintertools.png'))
        except TclError:
            print('\033[31mLoad tkintertools.png Error\033[0m')

    def canvas_3d_init(self):
        tkt.Button(
            self.canvas_3d, 10, 660, 200, 50, text='Back',
            command=lambda: (tkt.move(self.root, self.canvas_graph, 1280*self.canvas_main.rx, 0, 500, mode='rebound'),
                             tkt.move(self.root, self.canvas_3d, 1280*self.canvas_graph.rx, 0, 500, mode='rebound')))

        self.geos = []  # type: list[t3d.Geometry]

        for _ in range(10):
            # 创建正方体
            cube = t3d.Cuboid(
                self.canvas_3d, *sample(range(-200, 200), 3), *sample(range(50, 100), 3))
            self.geos.append(cube)
            # 创建四面体
            x, y, z = sample(range(-200, 200), 3)
            tetr = t3d.Tetrahedron(
                self.canvas_3d, *[[x+randint(-100, 100), y+randint(-100, 100), z+randint(-100, 100)] for _ in range(4)])
            self.geos.append(tetr)

        self.origin = t3d.Point(self.canvas_3d, [0, 0, 0], size=5)  # 原点
        self.axes = [t3d.Line(self.canvas_3d, [0, 0, 0], [100, 0, 0], width=3, fill='red'),  # 创建坐标轴
                     t3d.Line(self.canvas_3d, [0, 0, 0], [0, 100, 0],
                              width=3, fill='green'),
                     t3d.Line(self.canvas_3d, [0, 0, 0], [0, 0, -100], width=3, fill='blue')]

    def translate(self, event, flag=False, _cache=[]):
        # type: (Event, bool, list[float]) -> None
        """ 平移事件 """
        if flag:
            _cache[:] = [event.x, event.y]
            return
        dx = (event.x - _cache[0]) / 6
        dy = (event.y - _cache[1]) / 6
        _cache[:] = [event.x, event.y]
        for axis in self.axes:
            axis.translate(0, 6*dx, 6*dy)
            axis.update()
        for geo in self.geos:
            geo.translate(0, dx, dy)
            geo.update()
        self.origin.translate(0, 6*dx, 6*dy)
        self.origin.update()

    def rotate(self, event, flag=False, _cache=[]):
        # type: (Event, bool, list[float]) -> None
        """ 旋转事件 """
        if flag:
            _cache[:] = [event.x, event.y]
            return
        dy = (event.x - _cache[0]) / 200
        dx = (_cache[1] - event.y) / 200
        _cache[:] = [event.x, event.y]
        for item in self.axes:
            item.rotate(0, 6*dx, 6*dy, center=self.origin.coords)
            item.update()
        for item in self.geos:
            item.rotate(0, dx, dy, center=self.origin.coords)
            item.update()

    def scale(self, event):  # type: (Event) -> None
        """ 缩放事件 """
        k = 1.01 if event.delta > 0 else 0.99
        for geo in self.geos:
            geo.scale(k, k, k)
            geo.update()


if __name__ == '__main__':
    Application()
