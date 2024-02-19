"""Main codes of tkt-designer"""

import tkinter

from .. import core, shapes, widgets


class MenuBar(core.Canvas):
    """"""

    def build(self) -> None:
        """"""
        bg = "black" if self.master._theme["dark"] else "white"
        fg = "white" if self.master._theme["dark"] else "black"
        self.configure(height=40, bg=bg, highlightthickness=0)
        self.pack(anchor="n", expand=True, fill="x")
        menu_button = [
            widgets.Button(self, (5, 5), (75, 30), text="文件(F)"),
            widgets.Button(self, (85, 5), (75, 30), text="编辑(E)"),
            widgets.Button(self, (165, 5), (75, 30), text="视图(V)"),
            widgets.Button(self, (245, 5), (75, 30), text="设置(S)"),
            widgets.Button(self, (325, 5), (75, 30), text="帮助(H)"),
        ]
        for button in menu_button:
            button.text.configure(size=20)
            button.text.set_style(normal=fg, hover=fg, click=fg)
            if self.master._theme["dark"]:
                button.shape.set_style(normal=(bg, bg), hover=(
                    "#333", "#333"), click=("#333", "#777"))
                self.create_line(-5, 39, 2565, 39, fill="#333")
            else:
                button.shape.set_style(normal=(bg, bg), hover=(
                    "#CCC", "#CCC"), click=("#CCC", "#888"))
                self.create_line(-5, 39, 2565, 39, fill="#CCC")
            button.update()


class Work(core.Canvas):
    """"""

    def build(self) -> None:
        """"""
        bg = "#1F1F1F" if self.master._theme["dark"] else "#F1F1F1"
        self.configure(bg=bg, highlightthickness=0)
        self.place(width=1600, height=900, x=800, y=450, anchor="center")
        for x in range(0, 2560+1, 25):
            self.create_line(x, 0, x, 1600, fill="grey")
        for y in range(0, 1600+1, 25):
            self.create_line(0, y, 2560, y, fill="grey")


class StateBar(core.Canvas):
    """"""

    def build(self) -> None:
        """"""
        bg = "black" if self.master._theme["dark"] else "white"
        self.configure(height=30, bg=bg, highlightthickness=0)
        self.pack(anchor="s", expand=True, fill="x")
        state = widgets.Information(
            self, (5, 0), (80, 30), text="State: OK", shape=shapes.NoShape())
        state.text.configure(size=16)
        fg = "white" if self.master._theme["dark"] else "black"
        state.text.set_style(normal=fg, hover=fg, click=fg)
        state.update()
        if self.master._theme["dark"]:
            self.create_line(-5, 0, 2565, 0, fill="#333")
        else:
            self.create_line(-5, 0, 2565, 0, fill="#CCC")


class Application:
    """"""

    def __init__(
        self,
        *args,
    ) -> None:
        """"""
        self.root = core.Tk((1600, 900), title=f"Designer")
        # self.root.center()
        # self.root.theme(dark=False)
        Work(self.root, expand="xy", free_anchor=True).build()
        MenuBar(self.root, expand="").build()
        StateBar(self.root, expand="").build()
        # self.root.fullscreen()
