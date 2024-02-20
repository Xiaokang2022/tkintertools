"""Main codes of tkt-designer"""

import tkinter
from tkinter import messagebox, simpledialog

from .. import core, shapes, widgets


class InfoToplevel(core.Dialog):
    """"""


class MenuBar(core.Canvas):
    """"""

    def build(self) -> None:
        """"""
        bg = "black" if self.master._theme["dark"] else "white"
        fg = "white" if self.master._theme["dark"] else "black"
        self.configure(height=42, bg=bg, highlightthickness=0)
        self.pack(fill="x", side="top")
        menu_button = [
            widgets.Button(self, (5, 5), (75, 30), text="File"),
            widgets.Button(self, (85, 5), (75, 30), text="Edit"),
            widgets.Button(self, (165, 5), (75, 30), text="View"),
            widgets.Button(self, (245, 5), (75, 30), text="Set"),
            widgets.Button(self, (325, 5), (75, 30), text="Help",
                           command=lambda: InfoToplevel(Application.root, transient=True).center()),
        ]
        for button in menu_button:
            button.text.configure(size=20)
            button.text.set_style(normal=fg, hover=fg, click=fg)
            if self.master._theme["dark"]:
                button.shape.set_style(normal=(bg, bg), hover=(
                    "#333", "#333"), click=("#333", "#777"))
                self.create_line(-5, 41, 2565, 41, fill="#333")
            else:
                button.shape.set_style(normal=(bg, bg), hover=(
                    "#CCC", "#CCC"), click=("#CCC", "#888"))
                self.create_line(-5, 45, 2565, 45, fill="#CCC")
            button.update()


class Work(core.Canvas):
    """"""

    def build(self) -> None:
        """"""
        bg = "#1F1F1F" if self.master._theme["dark"] else "#F1F1F1"
        self.configure(bg=bg, highlightthickness=0)
        self.pack(fill="both", expand=True, anchor="center")
        for x in range(-1, 2561, 25):
            self.create_line(x, -1, x, 1601, fill="grey")
        for y in range(-1, 1601, 25):
            self.create_line(-1, y, 2561, y, fill="grey")


class StateBar(core.Canvas):
    """"""

    def build(self) -> None:
        """"""
        bg = "black" if self.master._theme["dark"] else "white"
        self.configure(height=30, bg=bg, highlightthickness=0)
        self.pack(fill="x", side="bottom")
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

    root = core.Tk((1600, 900), title=f"Designer")
    root.minsize(800, 600)
    root.center()

    def __init__(
        self,
        *args: str,
        **kw: str
    ) -> None:
        """"""
        self._parse_parameter(*args, **kw)
        # self.root.theme(dark=False)
        MenuBar(Application.root, expand="").build()
        Work(Application.root, expand="xy", free_anchor=True).build()
        StateBar(Application.root, expand="").build()
        # Application.root.fullscreen()

    def _parse_parameter(self, *args, **kw) -> None:
        """"""
        for i in range(0, len(args), 2):
            try:
                kw[args[i][1:]] = eval(args[i+1])
            except NameError:
                kw[args[i][1:]] = str(args[i+1])
        for k, v in kw.items():
            try:
                if method := getattr(Application.root, k, None):
                    method(v)
            except ValueError:
                pass
            try:
                Application.root.theme(**{k: v})
            except Exception:
                pass
