"""
Core codes of tkintertools

```text
    +-------+         +-------------+
    | tk.Tk |         | tk.Toplevel |
    +-------+         +-------------+
        |                    |           +------------------------+
        v                    v           |  Only works on Windows |
    +--------+        +--------------+   |    +--------------+    |
    | tkt.Tk | -----> | tkt.Toplevel | --+--> | tkt.NestedTk |    |
    +--------+        +--------------+   |    +--------------+    |
                                         |                        |
                                         +------------------------+

+-----------+        +------------+
| tk.Canvas | -----> | tkt.Canvas |
+-----------+        +------------+
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


class Tk(tkinter.Tk):
    """Main window"""

    def __init__(
        self,
        size: tuple[int, int] = (1280, 720),
        position: tuple[int, int] | None = None,
        *,
        title: str | None = "",
        iconbitmap: str | None = None,
        state: typing.Literal[
            "normal", "icon", "iconic", "withdrawn", "zoomed"] = "normal",
        alpha: float = 1,
        fullscreen: bool = False,
        toolwindow: bool = False,
        topmost: bool = False,
        transparentcolor: str = "",
        maxsize: tuple[int, int] | None = None,
        minsize: tuple[int, int] | None = None,
        resizable: tuple[bool, bool] = (True, True),
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

        self.bind("<Configure>", lambda _: self._zoom())

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

    def _zoom(self) -> None:
        """Zoom contents of the window"""
        if self._size != (size := [self.winfo_width(), self.winfo_height()]):
            relative_ratio = size[0] / self._size[0], size[1] / self._size[1]
            self._size = size
            self._ratio[0] = self._size[0] / self._initial_size[0]
            self._ratio[1] = self._size[1] / self._initial_size[1]
            for canvas in self._canvases:
                canvas._zoom(relative_ratio)

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
                HWND, 20, ctypes.byref(ctypes.c_int(dark)), 4)
        for i, value in enumerate((bordercolor, captioncolor, titlecolor)):
            if value is not None:
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    HWND, 34 + i, ctypes.byref(ctypes.c_int(color.str_to_hex(value, reverse=True))), 4)
        if background is not None:
            self["bg"] = background


class Toplevel(tkinter.Toplevel, Tk):
    """Toplevel window"""

    def __init__(
        self,
        master: Tk | typing.Self | "NestedTk" | None = None,
        size: tuple[int, int] = (960, 540),
        position: tuple[int, int] | None = None,
        *,
        title: str | None = None,
        iconbitmap: str | None = None,
        state: typing.Literal[
            "normal", "icon", "iconic", "withdrawn", "zoomed"] = "normal",
        alpha: float = 1,
        fullscreen: bool = False,
        toolwindow: bool = False,
        topmost: bool = False,
        transparentcolor: str = "",
        maxsize: tuple[int, int] | None = None,
        minsize: tuple[int, int] | None = None,
        resizable: tuple[bool, bool] = (True, True),
        overrideredirect: bool = False,
        transient: bool = False,
        focus: bool = True,
        shutdown: typing.Callable[[], typing.Any] | None = None,
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

    def __init__(
        self,
        master: Tk | Toplevel | typing.Self | None | "Canvas" = None,
        size: tuple[int, int] = (640, 360),
        position: tuple[int, int] | None = None,
        *,
        title: str | None = None,
        iconbitmap: str | None = None,
        state: typing.Literal[
            "normal", "icon", "iconic", "withdrawn", "zoomed"] = "normal",
        alpha: float = 1,
        toolwindow: bool = False,
        transparentcolor: str = "",
        maxsize: tuple[int, int] | None = None,
        minsize: tuple[int, int] | None = None,
        resizable: tuple[bool, bool] = (True, True),
        overrideredirect: bool = False,
        transient: bool = False,
        focus: bool = False,
        shutdown: typing.Callable[[], typing.Any] | None = None,
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


class Canvas(tkinter.Canvas):
    """Scalable Canvas"""

    def __init__(
        self,
        master: Tk | Toplevel | NestedTk | typing.Self,
        *,
        expand: typing.Literal["", "x", "y", "xy"] = "xy",
        keep_ratio: typing.Literal["min", "max", "full"] | None = None,
        free_anchor: bool = False,
        **kw,
    ) -> None:
        """
        #### Positional Arguments
        * `master`: parent widget
        #### Keyword-only Arguments
        * `size_expand`: expand mode of size of the Canvas
        * `position_expand`: expand mode of position of the Canvas
        #### Variable-length Keyword Arguments
        * `**kw`: compatible with other parameters of class tkinter.Canvas, see tkinter.Canvas for details
        """
        tkinter.Canvas.__init__(self, master, **kw)
        self._initial_size = [None, None]
        self._size = self._initial_size[:]
        self._initial_position = [None, None]
        self._position = self._initial_position[:]
        self._ratio = [1., 1.]

        self._canvases: list[Canvas] = []
        self._widgets: list[Widget] = []
        self._items: list[int] = []
        self._texts: dict[int, list[float]] = {}
        self._images: dict[int, list[tkinter.PhotoImage]] = {}

        self._expand = expand
        self._free_anchor = free_anchor
        self._keep_ratio = keep_ratio

        self.master._canvases.append(self)

        self.bind("<Motion>", self._event_touch)
        self.bind("<Any-Key>", self._event_input)
        self.bind("<Button-1>", self._event_click)
        self.bind("<B1-Motion>", self._event_click)
        self.bind("<MouseWheel>", self._event_wheel)
        self.bind("<ButtonRelease-1>", self._event_release)

    def get_canvases(self) -> tuple[typing.Self, ...]:
        """"""
        return tuple(self._canvases)

    def get_widgets(self) -> tuple["Widget", ...]:
        """"""
        return tuple(self._widgets)

    def get_items(self) -> tuple[int, ...]:
        """"""
        return tuple(self._items)

    def get_texts(self) -> tuple[int, ...]:
        """"""
        return tuple(self._texts)

    def get_images(self) -> tuple[int, ...]:
        """"""
        return tuple(self._images)

    def _zoom(self, relative_ratio: tuple[float, float]) -> None:
        """relative zooming for its contents"""
        if not self.winfo_viewable():
            return
        if self._initial_size == [None, None]:  # 未初始化
            self._initial_size = [self.winfo_width(), self.winfo_height()]

            anchor = self.place_info().get("anchor", None)
            if anchor == "nw" or anchor == None:
                dx = 0
                dy = 0
            elif anchor == "n":
                dx = self._initial_size[0] // 2
                dy = 0
            elif anchor == "w":
                dx = 0
                dy = self._initial_size[1] // 2
            elif anchor == "ne":
                dx = self._initial_size[0]
                dy = 0
            elif anchor == "sw":
                dx = 0
                dy = self._initial_size[1]
            elif anchor == "e":
                dx = self._initial_size[0]
                dy = self._initial_size[1] // 2
            elif anchor == "s":
                dx = self._initial_size[0]
                dy = self._initial_size[1] // 2
            elif anchor == "se":
                dx = self._initial_size[0]
                dy = self._initial_size[1]
            else:
                dx = self._initial_size[0] // 2
                dy = self._initial_size[1] // 2

            self._initial_position = [self.winfo_x()+dx, self.winfo_y()+dy]

        self._zoom_self()
        self._zoom_item(relative_ratio)
        self._zoom_text(relative_ratio)
        self._zoom_image(relative_ratio)

        for canvas in self._canvases:
            canvas._zoom(relative_ratio)

    def _zoom_self(self) -> None:
        """缩放画布自身"""
        if self.place_info():  # 仅 Place 布局
            if self._keep_ratio == "max":
                ratio_x = ratio_y = max(self.master._ratio)
            elif self._keep_ratio == "min":
                ratio_x = ratio_y = min(self.master._ratio)
            elif self._keep_ratio == "full":
                ratio_x = self.master._size[0] / self._initial_size[0]
                ratio_y = self.master._size[1] / self._initial_size[1]
                ratio_x = ratio_y = min(ratio_x, ratio_y)
            else:
                ratio_x, ratio_y = self.master._ratio
            if "x" in self._expand:
                self.place(width=self._initial_size[0]*ratio_x)
            if "y" in self._expand:
                self.place(height=self._initial_size[1]*ratio_y)
            if self._free_anchor:
                self.place(x=self._initial_position[0]*self.master._ratio[0],
                           y=self._initial_position[1]*self.master._ratio[1])

        self.update()
        self._position = [self.winfo_x(), self.winfo_y()]
        self._size = [self.winfo_width(), self.winfo_height()]
        self._ratio = [self._size[0] / self._initial_size[0],
                       self._size[1] / self._initial_size[1]]

    def _zoom_item(self, relative_ratio: tuple[float, float]) -> None:
        """元素位置缩放"""
        for item in self.find_all():
            self.coords(item, *[c * relative_ratio[i & 1]
                        for i, c in enumerate(self.coords(item))])

    def _zoom_text(self, relative_ratio: tuple[float, float]) -> None:
        """字体大小缩放"""
        for text, value in self._texts.items():
            value[1] *= math.sqrt(relative_ratio[0]*relative_ratio[1])
            font = value[:]
            font[1] = round(font[1])
            self.itemconfigure(text, font=font)

    def _zoom_image(self, relative_ratio: tuple[float, float]) -> None:
        """图像大小缩放（采用相对的绝对缩放）"""
        # for image, value in self._images.items():
        #     if value[0] and value[0].extension != "gif":
        #         value[1] = value[0].zoom(
        #             temp_x * rate_x, temp_y * rate_y, precision=1.2)
        #         self.itemconfigure(image, image=value[1])

    def _event_touch(self, event: tkinter.Event) -> None:
        """"""
        for widget in self._widgets[::-1]:
            if widget._touch(event):
                return
        else:
            self.configure(cursor="arrow")

    def _event_click(self, event: tkinter.Event) -> None:
        """"""
        self.focus_set()
        for widget in self._widgets[::-1]:
            if widget._click(event):
                return

    def _event_release(self, event: tkinter.Event) -> None:
        """"""
        for widget in self._widgets[::-1]:
            if widget._touch(event):
                return

    def _event_wheel(self, event: tkinter.Event) -> None:
        """"""
        for widget in self._widgets[::-1]:
            if widget._wheel(event):
                return

    def _event_input(self, event: tkinter.Event) -> None:
        """"""
        for widget in self._widgets[::-1]:
            if widget._input(event):
                return

    @typing.override
    def destroy(self) -> None:
        self.master._canvases.remove(self)
        return tkinter.Canvas.destroy(self)


"""
widget = shape + function + image/text
"""


class Shape:
    """Base Shape Class"""

    def __init__(
        self,
    ) -> None:
        pass

    def center(self) -> tuple[int, int]:
        """"""

    def position(self) -> tuple[int, int, int, int]:
        """"""


class Widget:
    """Base Widget Class"""

    def __init__(
        self,
        canvas: "Canvas",
        size: tuple[int, int],
        position: tuple[int, int],
        shape: Shape,
        text: str,
        image: None,
        through: bool,  # 能否透过
    ) -> None:
        """"""

    @typing.overload
    def state(self) -> str:
        pass

    @typing.overload
    def state(self, __state: typing.Literal['default', 'hover', 'selected', 'disabled', 'error']) -> None:
        pass

    def state(self, __state: typing.Literal['default', 'hover', 'selected', 'disabled', 'error'] | None = None) -> str | None:
        """"""

    def destroy(self) -> None:
        """"""

    def move(self, dx: int, dy: int) -> None:
        """"""

    def moveto(self, x: int, y: int) -> None:
        """"""

    def _touch(self, event: tkinter.Event) -> bool:
        """"""

    def _click(self, event: tkinter.Event) -> bool:
        """"""

    def _input(self, event: tkinter.Event) -> bool:
        """"""


class Dialog:
    """Base Dialog Class"""

    def __init__(
        self,
    ) -> None:
        pass


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
