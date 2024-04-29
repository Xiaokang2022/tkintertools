"""Main codes of tkt-designer"""

import pathlib
import tkinter
from tkinter import messagebox, simpledialog

from .. import constants, core, theme
from ..extra import widgets_ex
from ..standard import shapes, widgets

theme_folder = pathlib.Path(__file__).parent


class InfoToplevel(core.Dialog):
    """"""


class MenuBar(core.Canvas):
    """"""

    def build(self) -> None:
        """"""
        self.configure(
            height=42, bg="black" if self.master._theme["dark"] else "white", highlightthickness=0)
        self.pack(fill="x", side="top")

        widgets.Button(self, (5, 5), (75, 30), text="File", fontsize=20,
                       styles=theme.get("MenuButton", theme_folder)),
        widgets.Button(self, (85, 5), (75, 30), text="Edit", fontsize=20,
                       styles=theme.get("MenuButton", theme_folder)),
        widgets.Button(self, (165, 5), (75, 30), text="View", fontsize=20,
                       styles=theme.get("MenuButton", theme_folder)),
        widgets.Button(self, (245, 5), (75, 30), text="Set", fontsize=20,
                       styles=theme.get("MenuButton", theme_folder)),
        widgets.Button(self, (325, 5), (75, 30), text="Help", fontsize=20,
                       styles=theme.get("MenuButton", theme_folder),
                       command=lambda: InfoToplevel(Application.root, transient=True).center()),


class Work(core.Canvas):
    """"""

    def build(self) -> None:
        """"""
        bg = "#1F1F1F" if self.master._theme["dark"] else "#F1F1F1"
        self.configure(bg=bg, highlightthickness=0)
        self.pack(fill="both", expand=True, anchor="center")
        for x in range(-5, 2565, 32):
            self.create_line(x, -5, x, 1605, fill="grey")
        for y in range(-5, 1605, 32):
            self.create_line(-5, y, 2565, y, fill="grey")


class StateBar(core.Canvas):
    """"""

    def build(self) -> None:
        """"""
        self.configure(
            height=30, bg="black" if self.master._theme["dark"] else "white", highlightthickness=0)
        self.pack(fill="x", side="bottom")
        self.create_text(5, 15, text="State: OK", font=(
            constants.FONT, 20), anchor="w", fill="white" if self.master._theme["dark"] else "black")


class Application:
    """"""

    root = core.Tk((1600, 900), title=f"tkintertools")
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
