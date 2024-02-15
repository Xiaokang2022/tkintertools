"""
Core codes of tkintertools

Structure of Class:
```text
    +-------+         +-------------+
    | tk.Tk |         | tk.Toplevel |
    +-------+         +-------------+
        |                    |           +------------------------------+
        v                    v           |   Only works on Windows OS   |
    +--------+        +--------------+   |    +--------------------+    |
    | tkt.Tk | -----> | tkt.Toplevel | --+--> | tkt.NestedToplevel |    |
    +--------+        +--------------+   |    +--------------------+    |
                                         +------------------------------+
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

from . import _tools, color, constants

if platform.system() == "Windows":  # Set DPI awareness
    ctypes.WinDLL("shcore").SetProcessDpiAwareness(1)


class Tk(tkinter.Tk):
    """
    Main window

    In general, there is only one main window
    """

    def __init__(
        self,
        size: tuple[int, int] = (1280, 720),
        position: tuple[int, int] | None = None,
        *,
        title: str = "",
        **kw,
    ) -> None:
        """
        * `size`: the size of the window, default value is 1280x720(px)
        * `position`: the position of the window, default value indicates that the location is random
        * `title`: the title of the window, default value is an empty string
        * `**kw`: compatible with other parameters of class `tkinter.Tk`
        """
        if self.__class__ == Tk:  # NOTE: Subclasses of tkt.Tk do not inherit tk.Tk
            tkinter.Tk.__init__(self, **kw)

        self._initial_size = list(size)
        self._size = self._initial_size[:]
        self._ratio = [1., 1.]
        self._canvases: list[Canvas] = []
        self._theme: dict[str, str | bool | None] = self.master._theme if isinstance(
            self.master, tkinter.Wm) else {}

        self.title(title)
        self.theme(**self._theme)
        self.geometry(size=size, position=position)

        self.bind("<Configure>", lambda _: self._zoom())

    def geometry(
        self,
        *,
        size: tuple[int, int] | None = None,
        position: tuple[int, int] | None = None
    ) -> tuple[int, int, int, int] | None:
        """
        Change the size and position of the window and return the current size and position of the window

        * `size`: the size of the window, if it is None, does not change anything
        * `position`: the position of the window, if it is None, does not change anything
        """
        if size is not None and position is not None:
            self.wm_geometry(
                f"{size[0]}x{size[1]}+{position[0]}+{position[1]}")
        elif size is not None:
            self.wm_geometry(f"{size[0]}x{size[1]}")
        elif position is not None:
            self.wm_geometry(f"+{position[0]}+{position[1]}")
        return *self._size, self.winfo_x(), self.winfo_y()

    def get_canvases(self) -> tuple["Canvas", ...]:
        """Retrun all instances of `Canvas` of the window"""
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
        """Internal Method: Zoom contents of the window"""
        self.update()
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
        """
        Change the theme of the window

        * `dark`: whether it is in dark mode
        * `bordercolor`: window border color
        * `captioncolor`: window caption color
        * `titlecolor`: window title color
        * `background`: window background color

        ATTENTION: some parameter only works on Windows OS!
        """
        self.update()
        try:
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
        except:
            _tools._warning(
                "Some parameters are not available on the current OS!")
        if background is not None:
            self["bg"] = background
        self._theme.update(
            dark=dark, bordercolor=bordercolor, captioncolor=captioncolor,
            titlecolor=titlecolor, background=background)

    def alpha(self, value: float | None = None) -> float | None:
        """
        Set or get the transparency of the window

        * `value`: the transparency of the window, range is 0~1
        """
        return self.attributes("-alpha", value)

    def fullscreen(self, value: bool | None = None) -> bool | None:
        """
        Set or get whether the window is full-screen

        * `value`: indicate whether the window is full-screen
        """
        self.update()
        return bool(self.attributes("-fullscreen", value))

    def toolwindow(self, value: bool | None = None) -> bool | None:
        """
        Set or get whether the window is tool-window

        * `value`: indicate whether the window is tool-window
        """
        return bool(self.attributes("-toolwindow", value))

    def topmost(self, value: bool | None = None) -> bool | None:
        """
        Set or get whether the window is pinned or not

        * `value`: indicate whether the window is topmost
        """
        return bool(self.attributes("-topmost", value))

    def transparentcolor(self, value: str | None = None) -> str | None:
        """
        Set or get the penetration color of the window

        * `value`: the penetration color of the window
        """
        return self.attributes("-transparentcolor", value)

    def shutdown(self, func: typing.Callable | None, *args, **kw) -> None:
        """
        Set a function that will be called when the window is closed

        * `func`: the function that was called
        * `*args`: the variable-length argument of the called function
        * `**kw`: the keyword argument of the function being called

        ATTENTION: Regardless of whether the function is successfully called or not,
        the window will still close gracefully
        """
        def _wrapper() -> None:
            """Ensure that the window closes gracefully"""
            try:
                func(*args, **kw)
            finally:
                self.destroy()
        self.protocol("WM_DELETE_WINDOW", _wrapper)


class Toplevel(tkinter.Toplevel, Tk):
    """
    Toplevel window

    It can be used as a pop-up window, or it can be customized to put anything you want to show in it
    """

    def __init__(
        self,
        master: Tk | typing.Self | "NestedToplevel" | None = None,
        size: tuple[int, int] = (960, 540),
        position: tuple[int, int] | None = None,
        *,
        title: str | None = None,
        transient: bool = False,
        focus: bool = True,
        **kw,
    ) -> None:
        """
        * `master`: parent widget
        * `size`: the size of the window, default value is 960x540(px)
        * `position`: the position of the window, default value indicates that the location is random
        * `title`: title of window, default is the same as title of master
        * `transient`: instruct the window manager that this window is transient with regard to its master
        * `focus`: whether direct input focus to this window
        * `**kw`: compatible with other parameters of class `tkinter.Toplevel`
        """
        tkinter.Toplevel.__init__(self, master, **kw)
        Tk.__init__(self, size, position, title=title)
        if focus:
            self.focus_set()
        if transient:
            self.transient(self.master)


class NestedToplevel(Toplevel):
    """
    A window nested within another window

    ATTENTION: this CLASS only works on Windows OS
    """

    def __init__(
        self,
        master: Tk | Toplevel | typing.Self | "Canvas" | None = None,
        size: tuple[int, int] = (640, 360),
        position: tuple[int, int] | None = None,
        *,
        title: str | None = None,
        transient: bool = False,
        focus: bool = False,
        **kw,
    ) -> None:
        """
        * `master`: parent widget
        * `size`: the size of the window, default value is 640x360(px)
        * `position`: the position of the window, default value indicates that the location is random
        * `title`: title of window, default is the same as title of master
        * `transient`: instruct the window manager that this window is transient with regard to its master
        * `focus`: whether direct input focus to this window
        * `**kw`: compatible with other parameters of class `tkinter.Toplevel`
        """
        if platform.system() != "Windows":
            raise RuntimeError("This CLASS only works on Windows OS!")
        Toplevel.__init__(self, master, size, position,
                          title=title, transient=transient, **kw)
        self._handle = ctypes.windll.user32.GetParent(self.winfo_id())
        self._nested(self.master, focus=focus)

    def _nested(self, parent: tkinter.Misc | None = None, *, focus: bool = False) -> None:
        """
        Internal Method: Nest the window in its parent

        * `parent`: parent widget
        * `focus`: whether direct input focus to this window
        """
        ctypes.windll.user32.SetParent(
            self._handle, parent.winfo_id() if parent else None)
        if not focus:
            self.master.focus_set()


class Canvas(tkinter.Canvas):
    """
    Scalable Canvas

    The parent widget of all widgets of tkintertools is Canvas
    """

    def __init__(
        self,
        master: Tk | Toplevel | NestedToplevel | typing.Self,
        *,
        expand: typing.Literal["", "x", "y", "xy"] = "xy",
        keep_ratio: typing.Literal["min", "max", "full"] | None = None,
        free_anchor: bool = False,
        **kw,
    ) -> None:
        """
        * `master`: parent widget
        * `expand`: the mode of expand, `x` is horizontal, and `y` is vertical
        * `keep_ratio`: the mode of aspect ratio, `min` follows the minimum value,
        `max` follows the maximum value, and `full` follows the maximum possible value
        * `free_anchor`: whether the anchor point is free-floating
        * `**kw`: compatible with other parameters of class `tkinter.Canvas`
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
        """Retrun all child `Canvas` of the `Canvas`"""
        return tuple(self._canvases)

    def get_widgets(self) -> tuple["Widget", ...]:
        """Retrun all `Widget` of the `Canvas`"""
        return tuple(self._widgets)

    def get_items(self) -> tuple[int, ...]:
        """Retrun all items of the `Canvas`"""
        return tuple(self._items)

    def get_texts(self) -> tuple[int, ...]:
        """Retrun all texts of the `Canvas`"""
        return tuple(self._texts)

    def get_images(self) -> tuple[int, ...]:
        """Retrun all image of the `Canvas`"""
        return tuple(self._images)

    def _zoom(self, relative_ratio: tuple[float, float]) -> None:
        """Internal Method: Relative zooming for contents of the `Canvas`"""
        if not self.winfo_viewable():
            return
        if self._initial_size == [None, None]:
            self._size = self._initial_size = [
                self.winfo_width(), self.winfo_height()]

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

            self._position = self._initial_position = [
                self.winfo_x()+dx, self.winfo_y()+dy]

        relative_ratio = self._zoom_self()
        self._zoom_widgets(relative_ratio)
        self._zoom_items(relative_ratio)
        self._zoom_texts(relative_ratio)
        self._zoom_images(relative_ratio)

        for canvas in self._canvases:
            canvas._zoom(relative_ratio)

    def _zoom_self(self) -> tuple[float, float]:
        """Internal Method: Scale the `Canvas` itself, and return its own relative scale"""
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
        last_ratio = self._size[:]
        self._position = [self.winfo_x(), self.winfo_y()]
        self._size = [self.winfo_width(), self.winfo_height()]
        self._ratio = [self._size[0] / self._initial_size[0],
                       self._size[1] / self._initial_size[1]]
        return self._size[0] / last_ratio[0], self._size[1] / last_ratio[1]

    def _zoom_widgets(self, relative_ratio: tuple[float, float]) -> None:
        """控件数据修改"""
        for widget in self._widgets:
            widget.x1 *= relative_ratio[0]
            widget.x2 *= relative_ratio[0]
            widget.y1 *= relative_ratio[1]
            widget.y2 *= relative_ratio[1]

    def _zoom_items(self, relative_ratio: tuple[float, float]) -> None:
        """元素位置缩放"""
        for item in self.find_all():
            self.coords(item, *[c * relative_ratio[i & 1]
                        for i, c in enumerate(self.coords(item))])

    def _zoom_texts(self, relative_ratio: tuple[float, float]) -> None:
        """字体大小缩放"""
        for text, value in self._texts.items():
            value[1] *= math.sqrt(relative_ratio[0]*relative_ratio[1])
            font = value[:]
            font[1] = round(font[1])
            self.itemconfigure(text, font=font)

    def _zoom_images(self, relative_ratio: tuple[float, float]) -> None:
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
        # Override: 兼容原生 tkinter 的容器控件
        if _canvases := getattr(self.master, "_canvases", None):
            _canvases.remove(self)
        return tkinter.Canvas.destroy(self)

    @typing.override
    def create_text(self, *args, **kw) -> int:
        # Override: 添加对 text 类型的 _CanvasItemId 的字体大小的控制
        if not (font := kw.get("font")):
            kw["font"] = constants.FONT, constants.SIZE
        elif isinstance(font, str):
            kw["font"] = font, constants.SIZE
        elif isinstance(font, int):
            kw["font"] = constants.FONT, -abs(font)
        else:
            kw["font"] = list(kw["font"])
            kw["font"][1] = -kw["font"][1]
        text = tkinter.Canvas.create_text(self, *args, **kw)
        self._texts[text] = list(kw["font"])
        return text

    @typing.override
    def create_image(self, *args, **kw) -> int:
        # Override: 添加对 image 类型的 _CanvasItemId 的图像大小的控制
        image = tkinter.Canvas.create_image(self, *args, **kw)
        self._images[image] = [kw.get("image"), None]
        return image

    @typing.override
    def itemconfigure(self, tagOrId: str | int, **kw) -> dict[str, tuple[str, str, str, str, str]] | None:
        # Override: 创建空 image 的 _CanvasItemId 时漏去对图像大小的控制
        if kw.get("image").__class__ == tkinter.PhotoImage:
            self._image[tagOrId] = [kw.get("image"), None]
        return tkinter.Canvas.itemconfigure(self, tagOrId, **kw)


class Shape:
    """The Shape of a `Widget`"""

    def __init__(
        self,
        borderwidth: int,
        support_3d: bool = False
    ) -> None:
        self._size = [None, None]
        self._position = [None, None]

        self._items: list[int] = []

    def center(self) -> tuple[int, int]:
        """Return the geometric center of the `Shape`"""

    def position(self) -> tuple[int, int, int, int]:
        """"""

    def display(self, canvas: Canvas, size: tuple[int, int], position: tuple[int, int]) -> None:
        """"""

    def move(self, dx: int, dy: int) -> None:
        """"""

    def moveto(self, x: int, y: int) -> None:
        """"""

    def detect(self, x: int, y: int) -> bool:
        """"""


class Text:
    """The text of a `Widget`"""

    def __init__(
        self,
        text: str = "",
        *,
        font: tuple[str, int, str] | tuple[str, int] | str | int = (
            constants.FONT, constants.SIZE),
        justify: typing.Literal["left", "center", "right"] | None = None,
        angle: float = 0,
        color: tuple[str, str, str, str, str] = None,
        limit: int = -1,
        cursor: str = "|",
        show: str | None = None,
        read: bool = False,
        bbox: tuple[int, int, int, int] | None = None,
    ) -> None:
        """"""
        self._text = text
        self._font = font
        self._justify = justify
        self._angle = angle
        self._color = color

        self._instances: dict[int, Canvas] = {}

    def display(self, canvas: Canvas, position: tuple[int, int]) -> int:
        """"""
        item = canvas.create_text(*position, text=self._text, font=(
            self._font), justify=self._justify, fill=self._color[0], angle=self._angle)
        self._instances[item] = canvas
        return item

    def configure(
        self,
        *,
        text: str = "",
        font: tuple[str, int, str] | tuple[str, int] | str | int = (
            constants.FONT, constants.SIZE),
        justify: typing.Literal["left", "center", "right"] = "center",
        angle: float = 0,
        color: tuple[str, str, str, str, str] = None,
    ) -> None:
        """"""
        self._font = font
        self._justify = justify
        self._angle = angle
        self._color = color
        for item, canvas in self._instances.items():
            canvas.itemconfigure(
                item, text=text, font=font, justify=justify, angle=angle)

    def destroy(self, item: int | None = None) -> None:
        """"""
        if not self._instances:
            return
        if item:
            self._instances.pop(item).delete(item)
        else:
            for item, canvas in self._instances.items():
                canvas.delete(item)
            self._instances.clear()

    def get(self) -> str:
        """"""
        return self._text

    def set(self, text: str) -> None:
        """"""
        self.configure(text=text)

    def append(self, text: str) -> None:
        """"""

    def delete(self, num: int) -> None:
        """"""

    def clear(self) -> None:
        """"""


class Feature:
    """The features of a `Widget`"""


class Widget:
    """
    Base Widget Class

    `Widget` = [`Shape`] + [`Text`] + `Feature`
    """

    def __init__(
        self,
        canvas: Canvas,
        size: tuple[int, int],
        position: tuple[int, int],
        feature: Feature,
        *,
        shape: Shape,
        text: Text | str = "",
        image: tkinter.PhotoImage | None = None,
        through: bool = False,
        **kw,
    ) -> None:
        """"""
        self.master = canvas
        self.size = size
        self.position = position
        self._through = through

        self.shape = shape
        self.text = Text(text) if isinstance(text, str) else text
        self.image = image

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

    def configure(self) -> None:
        """"""

    def _touch(self, event: tkinter.Event) -> bool:
        """"""

    def _click(self, event: tkinter.Event) -> bool:
        """"""

    def _release(self, event: tkinter.Event) -> bool:
        """"""

    def _wheel(self, event: tkinter.Event) -> bool:
        """"""

    def _input(self, event: tkinter.Event) -> bool:
        """"""
