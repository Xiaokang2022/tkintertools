"""All standard Dialogs"""

import tkinter
import typing

from . import core


class Message(core.Dialog):
    """"""


def askfont(
    bind: typing.Callable[[str]] | None = None,
    initfont: str | tuple[str, int] | tuple[str, int, str] = ""
) -> None:
    """字体选择对话框，弹出选择字体的默认对话框窗口

    * `bind`: 关联的回调函数，有且仅有一个参数 `font`
    * `initfont`: 初始字体，格式为 `font` 参数默认格式

    注意: 由于 `tkinter` 模块无法直接打开该窗口，所以此处添加了这个函数
    """
    args = []

    if tkinter._default_root is None:
        tkinter.Tk().withdraw()

    if bind is not None:
        args += ["-command", tkinter._default_root.register(bind)]
    if initfont:
        if isinstance(initfont, tuple):
            initfont = " ".join(str(i) for i in initfont)
        args += ["-font", initfont]
    if args:
        tkinter._default_root.tk.call("tk", "fontchooser", "configure", *args)
    tkinter._default_root.tk.call("tk", "fontchooser", "show")


# class BaseToolTip(Toplevel):
#     """The base class of ToolTip"""

#     def __init__(
#         self,
#         *,
#         transparentcolor: str = TKDefault.TRANSPARENTCOLOR,
#         duration: int = 0,
#         animation: bool = False,
#         master: Tk | Toplevel | NestedTk | None = None,
#         **kw,
#     ) -> None:
#         """
#         #### Keyword only Arguments
#         * `transparentcolor`: a color in which the area of the window will become transparent
#         * `duration`: after duration ms, ToolTip will disappear
#         * `animation`: animation when appear and disappear
#         * `master`: parent widgets, not must
#         --------------------------------------
#         #### Variable length Keyword Arguments
#         * `**kw`: compatible with other parameters of class tkinter.Toplevel, see tkinter.Toplevel for details
#         """
#         Toplevel.__init__(
#             self, master, TKDefault.SIZE, TKDefault.POSITION, transparentcolor=transparentcolor,
#             resizable=(False, False), overrideredirect=True, **kw)
#         self.withdraw()
#         self.duration = duration
#         self.animation = animation

#     def show(self) -> None:
#         """show the ToolTip on the mouse"""
#         x, y = self.winfo_pointerxy()
#         self.geometry(f"+{x}+{y}")
#         if self.animation is True:
#             return self._animate(True)
#         self.deiconify()
#         if self.duration > 0:
#             self.after(self.duration, self._destroy)

#     def _destroy(self) -> None:
#         """destroy the ToolTip"""
#         if self.animation is True:
#             return self._animate(False)
#         self.destroy()

#     def _animate(self, start: bool) -> None:
#         """alpha change animation"""
#         # TODO: Need class Animation to code this!


# class ToolTip(BaseToolTip):
#     """A pop-up window"""

#     def __init__(
#         self,
#         text: str,
#         *,
#         font: tuple[str, int, str],
#         radius: int = 0,
#         fg: str = "black",
#         bg: str = "white",
#         frame_color: str = "grey",
#         justify: str = "center",
#         duration: int = 0,
#         animation: bool = False,
#         master: Tk | Toplevel | NestedTk | None = None,
#         **kw,
#     ) -> None:
#         """
#         #### Positional Arguments
#         * `text`: text of ToolTip
#         ---------------------------
#         #### Keyword only Arguments
#         * `font`: font of text
#         * `radius`: radius of ToolTip
#         * `fg`: foreground color
#         * `bg`: background color
#         * `frame_color`: frame color
#         * `justify`: justify mode of text
#         * `duration`: after duration ms, ToolTip will disappear
#         * `animation`: animation when appear and disappear
#         * `master`: parent widgets, not must
#         --------------------------------------
#         #### Variable length Keyword Arguments
#         * `**kw`: compatible with other parameters of class tkinter.Toplevel, see tkinter.Toplevel for details
#         """
#         BaseToolTip.__init__(
#             self,
#             master=master,
#             transparentcolor="888888",  # XXX: This color?
#             duration=duration,
#             animation=animation,
#             **kw,
#         )
#         # TODO: It maybe a std widget, should be moved to widgets.py?
