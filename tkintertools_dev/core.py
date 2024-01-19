"""
Core codes of tkintertools

```text
    +-------+         +-------------+
    | tk.Tk |         | tk.Toplevel |
    +-------+         +-------------+
        |                    |           +------------------------+
        v                    v           |  only work on Windows  |
    +--------+        +--------------+   |    +--------------+    |
    | tkt.Tk | -----> | tkt.Toplevel | --+--> | tkt.NestedTk |    |
    +--------+        +--------------+   |    +--------------+    |
                             |           |                        |
                             v           +------------------------+
+-------------+       +-----------------+
| tkt.ToolTip | <---- | tkt.BaseToolTip |
+-------------+       +-----------------+

+-----------+        +------------+
| tk.Canvas | -----> | tkt.Canvas |
+-----------+        +------------+

+----------------+        +---------+
| tkt.BaseWidget | =====> | Widgets |
+----------------+        +---------+
```
"""

import ctypes
import math
import platform
import tkinter
import typing

from . import _tools, color, constants, exceptions

if platform.system() == "Windows":  # Set DPI awareness
    ctypes.WinDLL("shcore").SetProcessDpiAwareness(1)


C_INT_SIZE = ctypes.sizeof(ctypes.c_int)


class Tk(tkinter.Tk):
    """Main window"""

    SIZE = 1280, 720
    POSITION = None
    TITLE = ""
    ICONBITMAP = None
    STATE = "normal"
    ALPHA = 1
    FULLSCREEN = False
    TOOLWINDOW = False
    TOPMOST = False
    TRANSPARENTCOLOR = ""
    MAXSIZE = None
    MINSIZE = None
    RESIZABLE = True, True
    OVERRIDEREDIRECT = False
    SHUTDOWN = None
    THEME = None

    def __init__(
        self,
        size: tuple[int, int] = SIZE,
        position: tuple[int, int] | None = POSITION,
        *,
        title: str | None = TITLE,
        iconbitmap: str | None = ICONBITMAP,
        state: typing.Literal[
            "normal", "icon", "iconic", "withdrawn", "zoomed"] = STATE,
        alpha: float = ALPHA,
        fullscreen: bool = FULLSCREEN,
        toolwindow: bool = TOOLWINDOW,
        topmost: bool = TOPMOST,
        transparentcolor: str = TRANSPARENTCOLOR,
        maxsize: tuple[int, int] | None = MAXSIZE,
        minsize: tuple[int, int] | None = MINSIZE,
        resizable: tuple[bool, bool] = RESIZABLE,
        overrideredirect: bool = None,
        shutdown: typing.Callable[[], typing.Any] | None = None,
        dark: bool | None = None,
        bordercolor: str | None = None,
        captioncolor: str | None = None,
        titlecolor: str | None = None,
        background: str | None = None,
        **kw,
    ) -> None:
        """
        Positional Arguments
        --------------------
        * `size`: size of window, default is 200x200(px)
        * `position`: position of window, default value indicates a center location, default indicates that position is centered

        Keyword only Arguments
        ----------------------
        * `title`: title of window
        * `iconbitmap`: path to the window icon file
        * `state`: state of the window
        * `alpha`: transparency of window, and the value is between 0~1, 0 is completely transparent
        * `fullscreen`: whether window is full screen
        * `toolwindow`: whether window is tool window
        * `topmost`: whether window is at the top
        * `transparentcolor`: a color in which the area of the window will become transparent
        * `maxsize`: maximum width and height of the window
        * `minsize`: minimum width and height of the window
        * `resizable`: whether the width and height of the window can be resized
        * `overrideredirect`: whether to remove window's borders and title bar
        * `shutdown`: a function that is called before closing the window, but it overrides the operation that originally closed the window

        Variable length Keyword Arguments
        ---------------------------------
        compatible with other parameters of class tkinter.Tk, see tkinter.Tk for details
        """
        if self.__class__ == Tk:  # NOTE: Subclasses of tkt.Tk do not inherit tk.Tk
            tkinter.Tk.__init__(self, **kw)

        self._initial_size = list(size)
        self._size = self._initial_size[:]
        self._ratio = [1., 1.]
        self._canvases: list[Canvas] = []

        self.title(title)
        self.state(state)
        if maxsize is not None:
            self.maxsize(*maxsize)
        if minsize is not None:
            self.minsize(*minsize)
        self.resizable(*resizable)
        self.iconbitmap(iconbitmap, iconbitmap)
        self.overrideredirect(overrideredirect)
        self.attributes("-alpha", alpha)
        self.attributes("-fullscreen", fullscreen)
        self.attributes("-toolwindow", toolwindow)
        self.attributes("-topmost", topmost)
        self.attributes("-transparentcolor", transparentcolor)
        self.protocol("WM_DELETE_WINDOW", shutdown)
        self.geometry(size=size, position=position)

        self.dark = dark
        self.bordercolor = bordercolor
        self.captioncolor = captioncolor
        self.titlecolor = titlecolor
        self.background = background

        self.theme(dark=dark, bordercolor=bordercolor, captioncolor=captioncolor,
                   titlecolor=titlecolor, background=background)

        self.bind("<Configure>", self._zoom)

    def geometry(
        self,
        *,
        size: tuple[int, int] | None = None,
        position: tuple[int, int] | None = None
    ) -> tuple[int, int, int, int] | None:
        """"""
        if size is not None and position is not None:
            self.wm_geometry(
                f"{size[0]}x{size[1]}+{position[0]}+{position[1]}")
        elif size is not None:
            self.wm_geometry(f"{size[0]}x{size[1]}")
        elif position is not None:
            self.wm_geometry(f"+{position[0]}+{position[1]}")
        return *self._size, self.winfo_x(), self.winfo_y()

    def get_canvases(self) -> tuple["Canvas"]:
        """Retrun all instances of Canvas of the window"""
        return tuple(self._canvases)

    def center(self) -> None:
        """Center the window"""
        self.update()
        if self.master is None or self.__class__ == Toplevel:
            parent_width = self.winfo_screenwidth()
            parent_height = self.winfo_screenheight()
        else:
            parent_width = self.master._size[0]
            parent_height = self.master._size[1]
        x = (parent_width - self._size[0]) // 2
        y = (parent_height - self._size[1]) // 2
        self.geometry(position=(x, y))

    def _zoom(self, event: tkinter.Event) -> None:
        """Zoom contents of the window"""
        if self._size != (size := [event.width, event.height]):
            self._size = size
            self._ratio[0] = self._size[0] / self._initial_size[0]
            self._ratio[1] = self._size[1] / self._initial_size[1]
            for canvas in self._canvases:
                canvas._zoom()

    def theme(
        self,
        *,
        dark: bool | None = None,
        bordercolor: str | None = None,
        captioncolor: str | None = None,
        titlecolor: str | None = None,
        background: str | None = None,
    ) -> None:
        """"""
        self.update()
        HWND = ctypes.windll.user32.GetParent(self.winfo_id())
        if dark is None:
            dark = _tools._is_dark()
        if dark is not None:
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                HWND, 20, ctypes.byref(ctypes.c_int(dark)), C_INT_SIZE)
        for i, value in enumerate((bordercolor, captioncolor, titlecolor)):
            if value is not None:
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    HWND, 34 + i, ctypes.byref(ctypes.c_int(color.str_to_hex(value, reverse=True))), C_INT_SIZE)
        if background is not None:
            self["bg"] = background


class Toplevel(tkinter.Toplevel, Tk):
    """Toplevel window"""

    SIZE = 960, 540
    POSITION = None
    TITLE = None
    ICONBITMAP = None
    STATE = "normal"
    ALPHA = 1
    FULLSCREEN = False
    TOOLWINDOW = False
    TOPMOST = False
    TRANSPARENTCOLOR = ""
    MAXSIZE = None
    MINSIZE = None
    RESIZABLE = True, True
    OVERRIDEREDIRECT = False
    TRANSIENT = False  # diffrent from Tk
    FOCUS = True  # diffrent from Tk
    SHUTDOWN = None
    THEME = None

    def __init__(
        self,
        master: Tk | typing.Self | "NestedTk" | None = None,
        size: tuple[int, int] = SIZE,
        position: tuple[int, int] | None = POSITION,
        *,
        title: str | None = TITLE,
        iconbitmap: str | None = ICONBITMAP,
        state: typing.Literal[
            "normal", "icon", "iconic", "withdrawn", "zoomed"] = STATE,
        alpha: float = ALPHA,
        fullscreen: bool = FULLSCREEN,
        toolwindow: bool = TOOLWINDOW,
        topmost: bool = TOPMOST,
        transparentcolor: str = TRANSPARENTCOLOR,
        maxsize: tuple[int, int] | None = MAXSIZE,
        minsize: tuple[int, int] | None = MINSIZE,
        resizable: tuple[bool, bool] = RESIZABLE,
        overrideredirect: bool = OVERRIDEREDIRECT,
        transient: bool = TRANSIENT,
        focus: bool = FOCUS,
        shutdown: typing.Callable[[], typing.Any] | None = SHUTDOWN,
        dark: bool | None = None,
        bordercolor: str | None = None,
        captioncolor: str | None = None,
        titlecolor: str | None = None,
        background: str | None = None,
        **kw,
    ) -> None:
        """
        #### Positional Arguments
        * `master`: parent widget
        * `size`: size of window, default is 200x200(px)
        * `position`: position of window, default value indicates that position is centered
        ---------------------------
        #### Keyword only Arguments
        * `title`: title of window, default is the same as title of master
        * `iconbitmap`: path to the window icon file
        * `state`: state of the window
        * `alpha`: transparency of window, and the value is between 0~1, 0 is completely transparent
        * `fullscreen`: whether window is full screen
        * `toolwindow`: whether window is tool window
        * `topmost`: whether window is at the top
        * `transparentcolor`: a color in which the area of the window will become transparent
        * `maxsize`: maximum width and height of the window
        * `minsize`: minimum width and height of the window
        * `resizable`: whether the width and height of the window can be resized
        * `overrideredirect`: whether to remove window's borders and title bar
        * `shutdown`: a function that is called before closing the window,
        but it overrides the operation that originally closed the window
        --------------------------------------
        #### Variable length Keyword Arguments
        compatible with other parameters of class tkinter.Toplevel, see tkinter.Toplevel for details
        """
        tkinter.Toplevel.__init__(self, master, **kw)
        Tk.__init__(
            self, size, position, title=title, iconbitmap=iconbitmap, alpha=alpha, state=state,
            fullscreen=fullscreen, toolwindow=toolwindow, topmost=topmost, transparentcolor=transparentcolor, maxsize=maxsize,
            minsize=minsize, resizable=resizable, overrideredirect=overrideredirect, shutdown=shutdown,
            dark=self.master.dark if dark is None else dark,
            bordercolor=self.master.bordercolor if bordercolor is None else bordercolor,
            captioncolor=self.master.captioncolor if captioncolor is None else captioncolor,
            titlecolor=self.master.titlecolor if titlecolor is None else titlecolor,
            background=self.master.background if background is None else background)
        if focus:
            self.focus_set()
        if transient:
            self.transient(self.master)


class NestedTk(Toplevel):
    """A window nested within another window"""

    SIZE = 640, 360
    POSITION = None
    TITLE = None
    ICONBITMAP = None
    STATE = "normal"
    ALPHA = 1
    TOOLWINDOW = False
    TRANSPARENTCOLOR = ""
    MAXSIZE = None
    MINSIZE = None
    RESIZABLE = True, True
    OVERRIDEREDIRECT = False
    SHUTDOWN = None
    TRANSIENT = False
    FOCUS = False

    def __init__(
        self,
        master: Tk | Toplevel | typing.Self | None | "Canvas" = None,
        size: tuple[int, int] = SIZE,
        position: tuple[int, int] | None = POSITION,
        *,
        title: str = TITLE,
        iconbitmap: str | None = ICONBITMAP,
        state: typing.Literal[
            "normal", "icon", "iconic", "withdrawn", "zoomed"] = STATE,
        alpha: float = ALPHA,
        toolwindow: bool = TOOLWINDOW,
        transparentcolor: str = TRANSPARENTCOLOR,
        maxsize: tuple[int, int] | None = MAXSIZE,
        minsize: tuple[int, int] | None = MINSIZE,
        resizable: tuple[bool, bool] = RESIZABLE,
        overrideredirect: bool = OVERRIDEREDIRECT,
        transient: bool = TRANSIENT,
        focus: bool = FOCUS,
        shutdown: typing.Callable[[], typing.Any] | None = SHUTDOWN,
        **kw,
    ) -> None:
        """
        #### Positional Arguments
        * `master`: parent widget
        * `size`: size of window, default is 200x200(px)
        * `position`: position of window, default value indicates that position is centered
        ---------------------------
        #### Keyword only Arguments
        * `title`: title of window, default is the same as title of master
        * `iconbitmap`: path to the window icon file
        * `state`: state of the window
        * `toolwindow`: whether window is tool window
        * `transparentcolor`: a color in which the area of the window will become transparent
        * `maxsize`: maximum width and height of the window
        * `minsize`: minimum width and height of the window
        * `resizable`: whether the width and height of the window can be resized
        * `overrideredirect`: whether to remove window's borders and title bar
        * `shutdown`: a function that is called before closing the window,
        but it overrides the operation that originally closed the window
        * `size_expand`: expand mode of size of nested window
        * `position_expand`: expand mode of position of nested window
        --------------------------------------
        #### Variable length Keyword Arguments
        * `**kw`: compatible with other parameters of class tkinter.Toplevel, see tkinter.Toplevel for details
        """
        if platform.system() != "Windows":
            raise RuntimeError("This CLASS only works on Windows OS!")
        Toplevel.__init__(
            self, master, size, position, title=title, iconbitmap=iconbitmap, toolwindow=toolwindow,
            maxsize=maxsize, minsize=minsize, resizable=resizable, overrideredirect=overrideredirect,
            shutdown=shutdown, transient=transient, **kw)
        self._nested(state, alpha, transparentcolor, focus)

    def _nested(
        self,
        state: typing.Literal["normal", "icon", "iconic", "withdrawn", "zoomed"],
        alpha: float,
        transparentcolor: bool,
        focus: bool
    ) -> None:
        """Nest the window in its parent"""
        handle = ctypes.windll.user32.GetParent(self.winfo_id())
        ctypes.windll.user32.SetParent(handle, self.master.winfo_id())
        self.state(state)
        self.attributes("-alpha", alpha)
        self.attributes("-transparentcolor", transparentcolor)
        if not focus:
            self.master.focus_set()


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


# class Canvas(tkinter.Canvas):
#     """Scalable Canvas"""

#     def __init__(
#         self,
#         master: typing.Union[Tk, Toplevel, "Canvas"],
#         *,
#         size_expand: BaseWidgetExpand = BaseWidgetExpand.XY,
#         position_expand: BaseWidgetExpand = BaseWidgetExpand.XY,
#         **kw,
#     ) -> None:
#         """
#         #### Positional Arguments
#         * `master`: parent widget
#         #### Keyword-only Arguments
#         * `size_expand`: expand mode of size of the Canvas
#         * `position_expand`: expand mode of position of the Canvas
#         #### Variable-length Keyword Arguments
#         * `**kw`: compatible with other parameters of class tkinter.Canvas, see tkinter.Canvas for details
#         """
#         tkinter.Canvas.__init__(self, master, **kw)
#         self.master = master
#         self.size_expand = size_expand
#         self.position_expand = position_expand
#         self._INIT_WIDTH: int = None
#         self._INIT_HEIGHT: int = None

#         self._nestedtks: list[NestedTk] = []
#         self._canvases: list[Canvas] = []
#         self._widgets: list[BaseWidget] = []
#         self._items: list[int] = []

#         self.master._canvases.append(self)

#         self.bind("<Motion>", self._touch)
#         self.bind("<Any-Key>", self._input)
#         self.bind("<Button-1>", self._click)
#         self.bind("<B1-Motion>", self._click)
#         self.bind("<MouseWheel>", self._mousewheel)
#         self.bind("<ButtonRelease-1>", self._release)
#         self.bind("<<Copy>>", self._copy)
#         self.bind("<<Paste>>", self._paste)
#         self.bind("<Configure>", self._zoom)

#     # HACK: Need code the position expand
#     def zoom(self, raito: tuple[float, float]) -> None:
#         """absolute zooming for itself"""
#         if "x" in self.size_expand.value:
#             self.width = int(self._INIT_WIDTH * raito[0])
#         if "y" in self.size_expand.value:
#             self.height = int(self._INIT_HEIGHT * raito[1])
#         self.place(width=self.width, height=self.height)

#     def _zoom(self, event: tkinter.Event) -> None:
#         """absolute zooming for its contents"""
#         if self._INIT_WIDTH is None:
#             self._INIT_WIDTH = event.width
#             self._INIT_HEIGHT = event.height
#             return

#         ratio_x = event.width / self._INIT_WIDTH
#         ratio_y = event.height / self._INIT_HEIGHT
#         for widget in self._widgets:
#             widget.scale_absolute(ratio_x, ratio_y)  # modify data

#         # modify contents
#         for item in self.find_withtag("x"):
#             self.coords(
#                 item,
#                 *[c * (ratio_x, 1)[i & 1]
#                   for i, c in enumerate(self.coords(item))],
#             )
#         for item in self.find_withtag("y"):
#             self.coords(
#                 item,
#                 *[c * (1, ratio_y)[i & 1]
#                   for i, c in enumerate(self.coords(item))],
#             )
#         for item in self.find_withtag("xy"):
#             self.coords(
#                 item,
#                 *[
#                     c * (ratio_x, ratio_y)[i & 1]
#                     for i, c in enumerate(self.coords(item))
#                 ],
#             )

#     def _touch(self, event):
#         # type: (tkinter.Event) -> None
#         """"""
#         for widget in self._widgets[::-1]:
#             if widget.state_hover(event):
#                 return
#         else:
#             self.configure(cursor="arrow")

#     def _click(self, event, _flag=False):
#         # type: (tkinter.Event, bool) -> None
#         """"""
#         for widget in self._widgets[::-1]:
#             if _flag:
#                 widget.state(BaseWidgetState.DEFAULT)
#             elif widget.state_selected(event):
#                 _flag = True

#     def _release(self, event):
#         # type: (tkinter.Event) -> None
#         """"""
#         for widget in self._widgets[::-1]:
#             if widget.state_hover(event):
#                 return

#     def _mousewheel(self, event):
#         # type: (tkinter.Event) -> None
#         """"""
#         for widget in self._widgets[::-1]:
#             if widget.scroll(event):
#                 return

#     def _input(self, event):
#         # type: (tkinter.Event) -> None
#         """"""
#         for widget in self._widgets[::-1]:
#             if widget.input(event):
#                 return

#     def _copy(self, event):
#         # type: (tkinter.Event) -> None
#         """"""
#         for widget in self._widgets[::-1]:
#             if widget.copy(event):
#                 return

#     def _paste(self, event):
#         # type: (tkinter.Event) -> None
#         """"""
#         for widget in self._widgets[::-1]:
#             if widget.paste(event):
#                 return

#     def _keep(self) -> None:
#         # type: () -> None
#         """"""
#         self.winfo_width()


# class BaseWidget:
#     """The base class for the widget class"""

#     def __init__(
#         self,
#         canvas,  # type: Canvas
#         x,  # type: int
#         y,  # type: int
#         width,  # type: int
#         height,  # type: int
#         /,
#         *,
#         resize=False,  # type: bool
#         minsize=(0, 0),  # type: tuple[int, int]
#         maxsize=(float("inf"), float("inf")),  # type: tuple[int, int]
#         expand=BaseWidgetExpand.XY,  # type: typing.Literal['', 'x', 'y', 'xy']
#         state=BaseWidgetState.DEFAULT,
#         # type: typing.Literal['default', 'hover', 'selected', 'disabled', 'error']
#     ) -> None:
#         """"""
#         self.canvas = canvas
#         self.resize = resize
#         self.expand = expand
#         self.minsize = minsize
#         self.maxsize = maxsize
#         self._state = state
#         self.x = self._init_x = x
#         self.y = self._init_y = y
#         self.width = self._init_width = width
#         self.height = self._init_height = height
#         self._items: dict[str, int] = {}
#         self.canvas._widgets.append(self)

#     def state(self, state_=None, /):
#         # type: (BaseWidgetState | None, ...) -> BaseWidgetState | None
#         """"""
#         if state_ is None:
#             return self._state
#         if state_ not in BaseWidgetState._value2member_map_:
#             raise StateError(state_)
#         self._state = state_
#         eval(f"self.state_{state_}()")  # XXX: It can be more Pythonic.

#     def destroy(self):
#         # type: () -> None
#         """"""
#         self.canvas.delete(*self._items.values())
#         self._items.clear()

#     def move(self, dx, dy):
#         # type: (int, int) -> None
#         """"""
#         self.x += dx
#         self.y += dy
#         for item in self._items.values():
#             self.canvas.move(item, dx, dy)

#     def move_to(self, x, y):
#         # type: (int, int) -> None
#         """"""
#         self.move(x - self.x, y - self.y)

#     def scale_absolute(self, ratio_x, ratio_y):
#         # type: (float, float) -> None
#         """"""
#         if "x" in self.expand:
#             self.x = self._init_x * ratio_x
#         if "y" in self.expand:
#             self.y = self._init_y * ratio_y
#         if self.resize is True:
#             self.width = self._init_width * ratio_x
#             self.height = self._init_height * ratio_y
#         self.scale_callback(ratio_x, ratio_y, "absolute")

#     def scale_relative(self, ratio_x, ratio_y):
#         # type: (float, float) -> None
#         """"""
#         if "x" in self.expand:
#             self.x *= ratio_x
#         if "y" in self.expand:
#             self.y *= ratio_y
#         if self.resize is True:
#             self.width *= ratio_x
#             self.height *= ratio_y
#         self.scale_callback(ratio_x, ratio_y, "relative")

#     def scale_callback(self, ratio_x, ratio_y, type_):
#         # type: (float, float, typing.Literal['absolute', 'relative']) -> None
#         """"""

#     def state_default(self, event):
#         # type: (tkinter.Event) -> bool
#         """"""
#         return False

#     def state_hover(self, event):
#         # type: (tkinter.Event) -> bool
#         """"""
#         return False

#     def state_selected(self, event):
#         # type: (tkinter.Event) -> bool
#         """"""
#         return False

#     def state_disabled(self, event):
#         # type: (tkinter.Event) -> bool
#         """"""
#         return False

#     def state_error(self, event):
#         # type: (tkinter.Event) -> bool
#         """"""
#         return False

#     def scroll(self, event):
#         # type: (tkinter.Event) -> bool
#         """"""
#         return False

#     def input(self, event):
#         # type: (tkinter.Event) -> bool
#         """"""
#         return False

#     def copy(self, event):
#         # type: (tkinter.Event) -> bool
#         """"""
#         return False

#     def paste(self, event):
#         # type: (tkinter.Event) -> bool
#         """"""
#         return False
