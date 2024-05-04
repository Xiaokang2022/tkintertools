"""
Core codes of tkintertools

Structure of Class:
```text
+-------+       +-------------+
| tk.Tk |       | tk.Toplevel |
+-------+       +-------------+
    |                  |          +--------------------------+
    v                  v          |   Only works on Windows  |
+--------+      +--------------+  |   +--------------------+ |
| tkt.Tk | ---> | tkt.Toplevel | -+-> | tkt.NestedToplevel | |
+--------+      +--------------+  |   +--------------------+ |
                       |          +--------------------------+
                       v
                +------------+
                | tkt.Dialog |
                +------------+

+-----------+        +------------+
| tk.Canvas | -----> | tkt.Canvas |
+-----------+        +------------+

               +------------+
               | Image, ... |
               +------------+
                     |
                     v
+---------+      +--------+      +-----------+
| Feature | ---> | Widget | <--- | Text, ... |
+---------+      +--------+      +-----------+
                     ^
                     |
               +------------+
               | Shape, ... |
               +------------+
```
"""

import abc
import copy
import ctypes
import math
import pathlib
import platform
import threading
import tkinter
import tkinter.font as font
import typing

import darkdetect

from . import color, constants, exceptions, style
from .animate import animations

type State = str | int
type Tag = str | int
type Style = dict[Tag, dict[str, str]]


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

        self._initial_size: tuple[int, int] = list(size)
        self._size: tuple[int, int] = self._initial_size[:]
        self._ratio: tuple[float, float] = [1., 1.]
        self._canvases: list[Canvas] = []
        self._theme: dict[str, str | bool | None] = self.master._theme if isinstance(
            self.master, tkinter.Wm) else {}

        self.title(title)
        self.theme(**self._theme)
        self.geometry(size=size, position=position)
        threading.Thread(target=darkdetect.listener, args=(
            lambda theme: self._switch_theme(theme == "Dark"),), daemon=True).start()

        self.bind("<Configure>", lambda _: self._zoom())

    @typing.override
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
        # self.update()  # ALPHA: What is the chance that the center will fail without this line of code?
        if self.master is None or self.__class__ == Toplevel:
            parent_width = self.winfo_screenwidth()
            parent_height = self.winfo_screenheight()
        else:
            parent_width = self.master.winfo_width()
            parent_height = self.master.winfo_height()

        x = (parent_width - self._size[0]) // 2
        y = (parent_height - self._size[1]) // 2
        self.geometry(position=(x, y))

    def _zoom(self) -> None:
        """Internal Method: Zoom contents of the window"""
        # self.update()  # ALPHA
        if self._size != (size := [self.winfo_width(), self.winfo_height()]):
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
                dark = darkdetect.isDark()
            if dark is not None:
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    HWND, 20, ctypes.byref(ctypes.c_int(dark)), 4)
                if background is None:
                    background = "#1F1F1F" if dark else "#F1F1F1"
            for i, value in enumerate((bordercolor, captioncolor, titlecolor)):
                if value is not None:
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        HWND, 34 + i, ctypes.byref(ctypes.c_int(color.str_to_hex(value, reverse=True))), 4)
        except:
            exceptions._warning(
                f"Some parameters are not available on the current OS({platform.system()})!")
        if background is not None:
            self["bg"] = background
        self._theme.update(
            dark=dark, bordercolor=bordercolor, captioncolor=captioncolor,
            titlecolor=titlecolor, background=background)

    def _switch_theme(self, dark: bool) -> None:
        """"""
        self.theme(dark=dark)
        for container in self.children:
            if isinstance(container, Toplevel):
                container._switch_theme(dark=dark)
        for canvas in self._canvases:
            canvas["bg"] = canvas.master["bg"]
            canvas["insertbackground"] = "white" if dark else "black"
            for widget in canvas._widgets:
                for component in widget.shapes + widget.texts + widget.images:
                    if styles := style.get(widget, component):
                        component.styles = styles
                widget.update()

    def alpha(self, value: float | None = None) -> float | None:
        """
        Set or get the transparency of the window

        * `value`: the transparency of the window, range is 0~1
        """
        return self.attributes("-alpha", value)

    def fullscreen(self, value: bool | None = True) -> bool | None:
        """
        Set or get whether the window is full-screen

        * `value`: indicate whether the window is full-screen

        ATTENTION: This method should be called later
        """
        self.update()
        if value is None:
            return bool(self.attributes("-fullscreen"))
        self.attributes("-fullscreen", value)
        if not value:  # When you cancel the full-screen state, the `theme` method is invalidated
            self.theme(**self._theme)

    def toolwindow(self, value: bool | None = True) -> bool | None:
        """
        Set or get whether the window is tool-window

        * `value`: indicate whether the window is tool-window
        """
        return bool(self.attributes("-toolwindow", value))

    def topmost(self, value: bool | None = True) -> bool | None:
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
        grab: bool = False,
        focus: bool = True,
        **kw,
    ) -> None:
        """
        * `master`: parent widget
        * `size`: the size of the window, default value is 960x540(px)
        * `position`: the position of the window, default value indicates that the location is random
        * `title`: title of window, default is the same as title of master
        * `transient`: instruct the window manager that this window is transient with regard to its master
        * `grab`: set grab for this window
        * `focus`: whether direct input focus to this window
        * `**kw`: compatible with other parameters of class `tkinter.Toplevel`
        """
        tkinter.Toplevel.__init__(self, master, **kw)
        if transient:
            self.transient(self.master)
        Tk.__init__(self, size, position, title=title)
        if grab:
            self.grab_set()
        if focus:
            self.focus_set()


class Dialog(Toplevel):
    """"""

    def __init__(
        self,
        master: Tk | typing.Self | "NestedToplevel" | None = None,
        size: tuple[int, int] = (720, 405),
        position: tuple[int, int] | None = None,
        *,
        title: str | None = None,
        transient: bool = False,
        **kw,
    ) -> None:
        """
        * `master`: parent widget
        * `size`: the size of the window, default value is 960x540(px)
        * `position`: the position of the window, default value indicates that the location is random
        * `title`: title of window, default is the same as title of master
        * `transient`: instruct the window manager that this window is transient with regard to its master
        * `**kw`: compatible with other parameters of class `tkinter.Toplevel`
        """
        Toplevel.__init__(self, master, size, position, title=title,
                          transient=transient, grab=True, focus=True, **kw)
        self.bind("<Button-1>", self._bell, "+")

    @typing.override
    def center(self) -> None:
        if self.master is not None:
            x = (self.master.winfo_width() -
                 self._size[0]) // 2 + self.master.winfo_x()
            y = (self.master.winfo_height() -
                 self._size[1]) // 2 + self.master.winfo_y()
        else:
            x = (self.winfo_screenwidth() - self._size[0]) // 2
            y = (self.winfo_screenheight() - self._size[1]) // 2
        self.geometry(position=(x, y))

    def _bell(self, event: tkinter.Event) -> None:
        """Internal Method: When an attempt is made to move out of focus, a bell prompts the user"""
        if not 0 <= event.x <= self._size[0] or not 0 <= event.y <= self._size[1]:
            self.bell()


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
        zoom_item: bool = False,
        keep_ratio: typing.Literal["min", "max", "full"] | None = None,
        free_anchor: bool = False,
        **kw,
    ) -> None:
        """
        * `master`: parent widget
        * `expand`: the mode of expand, `x` is horizontal, and `y` is vertical
        * `zoom_item`: whether or not to scale its items
        * `keep_ratio`: the mode of aspect ratio, `min` follows the minimum value,
        `max` follows the maximum value, and `full` follows the maximum possible value
        * `free_anchor`: whether the anchor point is free-floating
        * `**kw`: compatible with other parameters of class `tkinter.Canvas`
        """
        tkinter.Canvas.__init__(self, master, **kw)

        self._initial_size: tuple[int, int] = [None, None]
        self._size: tuple[int, int] = self._initial_size[:]
        self._initial_position: tuple[int, int] = [None, None]
        self._position: tuple[int, int] = self._initial_position[:]
        self._ratio: tuple[float, float] = [1., 1.]

        self._canvases: list[Canvas] = []
        self._widgets: list[Widget] = []
        self._items: list[int] = []
        self._texts: dict[int, list[font.Font | int]] = {}
        self._images: dict[int, list[Image]] = {}

        self._expand = expand
        self._zoom_item = zoom_item
        self._free_anchor = free_anchor
        self._keep_ratio = keep_ratio

        if kw.get("bg") is None:
            self["bg"] = master["bg"]
        if kw.get("highlightthickness") is None:
            self["highlightthickness"] = 0
        if kw.get("insertbackground") is None:
            self["insertbackground"] = "white" if master._theme["dark"] else "black"

        self.master._canvases.append(self)

        self.bind("<Any-Key>", self._input)

        if platform.system() == "Linux":
            self.bind("<Button-4>", lambda event: self._wheel(event, "up"))
            self.bind("<Button-5>", lambda event: self._wheel(event, "down"))
        else:
            self.bind("<MouseWheel>", self._wheel)

        self.bind("<Button-1>", lambda event: self._click(event, "left"))
        self.bind("<Button-2>", lambda event: self._click(event, "center"))
        self.bind("<Button-3>", lambda event: self._click(event, "right"))

        self.bind("<Motion>", lambda event: self._move(event, "none"))
        self.bind("<B1-Motion>", lambda event: self._move(event, "left"))
        self.bind("<B2-Motion>", lambda event: self._move(event, "center"))
        self.bind("<B3-Motion>", lambda event: self._move(event, "right"))

        self.bind("<ButtonRelease-1>",
                  lambda event: self._release(event, "left"))
        self.bind("<ButtonRelease-2>",
                  lambda event: self._release(event, "center"))
        self.bind("<ButtonRelease-3>",
                  lambda event: self._release(event, "right"))

        self.bind("<Configure>", lambda _: self._zoom_self())

        self.focus_set()

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

    def _zoom_init(self) -> None:
        """Internal Method: Scale initialization"""
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

    def _zoom(self) -> None:
        """Internal Method: Relative zooming for contents of the `Canvas`"""
        if not self.winfo_viewable():
            return
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

    def _zoom_self(self) -> None:
        """Internal Method: Scale the `Canvas` itself, and return its own relative scale"""
        if self._initial_size == [None, None]:
            self._zoom_init()
        last_ratio = self._size[:]
        self._position = [self.winfo_x(), self.winfo_y()]
        self._size = [self.winfo_width(), self.winfo_height()]
        self._ratio = [self._size[0] / self._initial_size[0],
                       self._size[1] / self._initial_size[1]]

        if self._zoom_item:
            relative_ratio = self._size[0] / \
                last_ratio[0], self._size[1] / last_ratio[1]
            self._zoom_widgets(relative_ratio)
            self._zoom_items(relative_ratio)
            self._zoom_texts(relative_ratio)
            self._zoom_images(relative_ratio)

        for canvas in self._canvases:
            canvas._zoom()

    def _zoom_widgets(self, relative_ratio: tuple[float, float]) -> None:
        """Internal Method: Modify data for the position and size of the widgets"""
        for widget in self._widgets:
            widget.w *= relative_ratio[0]
            widget.h *= relative_ratio[1]
            widget.x *= relative_ratio[0]
            widget.y *= relative_ratio[1]
            for component in widget.shapes + widget.texts + widget.images:
                component.w *= relative_ratio[0]
                component.h *= relative_ratio[1]
                component.x *= relative_ratio[0]
                component.y *= relative_ratio[1]

    def _zoom_items(self, relative_ratio: tuple[float, float]) -> None:
        """Internal Method: Scale the items"""
        for item in self.find_all():
            self.scale(item, 0, 0, *relative_ratio)

    def _zoom_texts(self, relative_ratio: tuple[float, float]) -> None:
        """Internal Method: Scale the texts"""
        for text, value in self._texts.items():
            value[0] *= math.sqrt(relative_ratio[0]*relative_ratio[1])
            value[1].config(size=round(value[0]))
            self.itemconfigure(text, font=value[1])

    def _zoom_images(self, relative_ratio: tuple[float, float]) -> None:
        """Internal Method: Scale the images"""
        # for image, value in self._images.items():
        #     if value[0] and value[0].extension != "gif":
        #         value[1] = value[0].zoom(
        #             temp_x * rate_x, temp_y * rate_y, precision=1.2)
        #         self.itemconfigure(image, image=value[1])

    @typing.override
    def destroy(self) -> None:
        if _canvases := getattr(self.master, "_canvases", None):
            _canvases.remove(self)
        return tkinter.Canvas.destroy(self)

    @typing.override  # 添加对 text 类型的 _CanvasItemId 的字体大小的控制
    def create_text(self, *args, **kw) -> int:
        if not (font_ := kw.get("font")):
            kw["font"] = font.Font(family=constants.FONT, size=constants.SIZE)
        elif isinstance(font_, str):
            kw["font"] = font.Font(family=font_, size=constants.SIZE)
        elif isinstance(font_, int):
            kw["font"] = font.Font(family=constants.FONT, size=-abs(font_))
        elif isinstance(font_, font.Font):
            kw["font"].config(size=-abs(font_.cget("size")))
        else:
            font_ = list(font_)
            font_[1] = -abs(font_[1])
            length = len(font_)
            kw["font"] = font.Font(family=font_[0], size=font_[1],
                                   weight=font_[2] if length > 2 else "normal",
                                   slant=font_[3] if length > 3 else "roman")
            # XXX
        text = tkinter.Canvas.create_text(self, *args, **kw)
        self._texts[text] = [kw["font"].cget("size"), kw["font"]]
        return text

    @typing.override  # 添加对 image 类型的 _CanvasItemId 的图像大小的控制
    def create_image(self, *args, **kw) -> int:
        image = tkinter.Canvas.create_image(self, *args, **kw)
        self._images[image] = [kw.get("image"), None]
        if self._images[image][0].__class__ == Image:
            self._images[image][0] = self._images[image][0].items
        return image

    @typing.override  # 创建空 image 的 _CanvasItemId 时漏去对图像大小的控制
    def itemconfigure(self, tagOrId: str | int, **kw) -> dict[str, tuple[str, str, str, str, str]] | None:
        if kw.get("image").__class__ == Image:
            self._images[tagOrId] = [kw.get("image"), None]
        return tkinter.Canvas.itemconfigure(self, tagOrId, **kw)

    def _move(
        self,
        event: tkinter.Event,
        type_: typing.Literal["left", "center", "right", "none"]
    ) -> None:
        """Internal Method: Events to move the mouse"""
        for widget in self.get_widgets()[::-1]:
            if getattr(widget.feature, f"_move_{type_}", lambda _: False)(event) or widget.through:
                return
        if self.cget("cursor") != "arrow":
            self.configure(cursor="arrow")

    def _click(
        self,
        event: tkinter.Event,
        type_: typing.Literal["left", "center", "right"]
    ) -> None:
        """Internal Method: Events to click the mouse"""
        for widget in self.get_widgets()[::-1]:
            if getattr(widget.feature, f"_click_{type_}", lambda _: False)(event):
                if widget.through:
                    continue
                return

    def _release(
        self,
        event: tkinter.Event,
        type_: typing.Literal["left", "center", "right"]
    ) -> None:
        """Internal Method: Events to release the mouse"""
        for widget in self.get_widgets()[::-1]:
            if getattr(widget.feature, f"_release_{type_}", lambda _: False)(event):
                if widget.through:
                    continue
                return

    def _wheel(
        self,
        event: tkinter.Event,
        type_: typing.Literal["up", "down"] | None = None
    ) -> None:
        """Internal Method: Events to scroll the mouse wheel"""
        if type_ is not None:
            event.delta = 120 if type_ == "up" else -120
        for widget in self.get_widgets()[::-1]:
            if getattr(widget.feature, "_wheel", lambda _: False)(event):
                if widget.through:
                    continue
                return

    def _input(self, event: tkinter.Event) -> None:
        """Internal Method: Events for typing"""
        for widget in self.get_widgets()[::-1]:
            if getattr(widget.feature, "_input", lambda _: False)(event):
                if widget.through:
                    continue
                return


class Feature(abc.ABC):
    """Base Class: The features of a `Widget`"""

    def __init__(self, widget: "Widget") -> None:
        self.widget: Widget = widget
        widget.feature = self

    def _move_none(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of moving the mouse"""
        return False

    def _move_left(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of holding down the left mouse button to move the mouse"""
        return False

    def _move_center(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of holding down the center mouse button to move the mouse"""
        return False

    def _move_right(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of holding down the right mouse button to move the mouse"""
        return False

    def _click_left(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of pressing the left mouse button"""
        return False

    def _click_center(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of pressing the center mouse button"""
        return False

    def _click_right(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of pressing the right mouse button"""
        return False

    def _release_left(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of releasing the left mouse button"""
        return False

    def _release_center(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of releasing the center mouse button"""
        return False

    def _release_right(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of releasing the right mouse button"""
        return False

    def _wheel(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of scrolling the mouse wheel"""
        return False

    def _input(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of typing"""
        return False


class Component(abc.ABC):
    """The basic part of a `Widget`"""

    def __init__(
        self,
        widget: "Widget",
        rel_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        name: str | None = None,
        styles: dict[State, Style] | None = None,
    ) -> None:
        self.widget: Widget = widget
        self.x = rel_position[0] + widget.x
        self.y = rel_position[1] + widget.y
        self.w, self.h = size if size else (widget.w, widget.h)
        self.name: str = name
        self.styles = styles if styles else style.get(widget, self)
        self.items: list[int] = []
        self.visible: bool = True
        widget.register(self)

    def move(self, dx: int, dy: int) -> None:
        """Move the `Component`"""
        self.x += dx
        self.y += dy
        for item in self.items:
            self.widget.master.move(item, dx, dy)

    def moveto(self, x: int, y: int) -> None:  # BUG: can't use twice!
        """Move the `Component` to a certain position"""
        return self.move(x - self.x, y - self.y)

    def destroy(self) -> None:
        """Destroy the `Component`"""
        self.widget.master.delete(*self.items)

    def center(self) -> tuple[int, int]:
        """Return the geometric center of the `Component`"""
        return self.x + self.w/2, self.y + self.h/2

    def region(self) -> tuple[int, int, int, int]:
        """Return the decision region of the `Component`"""
        return self.x, self.y, self.x + self.w, self.y + self.h

    def detect(self, position: tuple[int, int]) -> bool:
        """
        Detect whether the specified coordinates are within the `Component`

        * `position`: the specified coordinates
        """
        x1, y1, x2, y2 = self.region()
        return x1 <= position[0] <= x2 and y1 <= position[1] <= y2

    def update(self, state: State | None = None, *, no_delay: bool = False) -> None:
        """
        Update the style of the `Component` to the corresponding state

        * `state`: the state of the `Component`
        """
        if state is None:
            state = self.widget.state
        if self.styles.get(state) is not None and self.visible:
            self.configure(self.styles[state], no_delay=no_delay)

    def configure(self, style: Style, *, no_delay: bool = False) -> None:
        """Configure properties of the `Component` and update them immediately"""
        for item in self.items:
            for tag in self.widget.master.itemcget(item, "tag").split():
                if (kwargs := style.get(tag)) is not None:
                    if self.widget.animation and not no_delay:
                        for key, value in kwargs.items():
                            animations.Gradient(
                                self.widget.master, item, key, 150, delta=value).start()
                    else:
                        self.widget.master.itemconfigure(item, **kwargs)

    def appear(self, *, no_delay: bool = True) -> None:
        """"""
        self.visible = True
        self.update(self.widget.state, no_delay=no_delay)

    def disappear(self, *, no_delay: bool = True) -> None:
        """"""
        self.visible = False
        temp_style = copy.deepcopy(self.styles[self.widget.state])
        for style in temp_style.values():
            for arg in style:
                style[arg] = ""
        self.configure(temp_style, no_delay=no_delay)

    @abc.abstractmethod
    def zoom(self, ratio: tuple[float, float]) -> None:
        """Scale the `Component`"""

    @abc.abstractmethod
    def display(self) -> None:
        """Display the `Component` on a `Canvas`"""


class Shape(Component):
    """
    Base Class: The Shape of a `Widget`

    You can view all of its standard derivatives in file: shapes.py
    """

    def zoom(self, ratio: tuple[float, float]) -> None:
        """Scale the items"""
        for item in self.items:
            self.widget.master.scale(item, 0, 0, *ratio)


class Text(Component):
    """Base Class: The text of a `Widget`"""

    def __init__(
        self,
        widget: "Widget",
        *,
        styles: dict[State, Style] | None = None,
        text: str = "",
        family: str = constants.FONT,
        size: int = constants.SIZE,
        weight: typing.Literal["normal", "bold"] = "normal",
        slant: typing.Literal["roman", "italic"] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        limit: int = math.inf,
    ) -> None:
        """
        * `text`: the value of `Text`
        * `limit`: the limitation of value length
        """
        self.value: str = text
        self.limit: int = limit
        self.font: font.Font = font.Font(
            family=family, size=-abs(size), weight=weight, slant=slant,
            underline=underline, overstrike=overstrike)
        return Component.__init__(self, widget, styles=styles)

    def region(self) -> tuple[int, int, int, int]:
        """Return the decision region of the `Text`"""
        width_half = self.font.measure(self.value)/2
        height_half = -self.font.cget("size") / 2
        x, y = self.center()
        return x-width_half, y-height_half, x+width_half, y+height_half

    def zoom(self, ratio: tuple[float, float]) -> None:
        """Scale the text"""
        for item in self.items:
            value = self.widget.master._texts[item]
            value[0] *= math.sqrt(ratio[0]*ratio[1])
            value[1].config(size=round(value[0]))
            self.widget.master.itemconfigure(item, font=value[1])
            self.widget.master.scale(item, 0, 0, *ratio)

    def get(self) -> str:
        """Get the value of `Text`"""
        return self.value

    def set(self, text: str) -> None:
        """Set the value of `Text`"""
        if len(text) > self.limit:
            raise ValueError
        self.value = text
        self.widget.master.itemconfigure(self.items[0], text=self.value)

    def append(self, text: str) -> None:
        """Append value to the value of `Text`"""
        if len(self.value) + len(text) > self.limit:
            raise ValueError
        self.value = self.value + text
        self.widget.master.itemconfigure(self.items[0], text=self.value)

    def delete(self, num: int) -> None:
        """Remove a portion of the `Text` value from the trail"""
        if num > len(self.value):
            raise ValueError
        self.value = self.value[:-num]
        self.widget.master.itemconfigure(self.items[0], text=self.value)

    def clear(self) -> None:
        """Clear the value of `Text`"""
        self.value = ""
        self.widget.master.itemconfigure(self.items[0], text=self.value)


class Image(Component):
    """Base Class: an image of a `Widget`"""

    def __init__(
        self,
        widget: "Widget",
        *,
        file: str = "",
        styles: dict[State, Style] | None = None
    ) -> None:
        """"""
        self.file = file
        self.extension = pathlib.Path(file).suffix
        return Component.__init__(self, widget, styles=styles)

    def zoom(self, ratio: tuple[float, float]) -> None:
        """"""


class Widget:
    """
    Base Widget Class

    `Widget` = `Shape` + `Text` + `Image` + `Feature`
    """

    def __init__(
        self,
        master: Canvas,
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        state: State = "normal",
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """"""
        self.master = master
        self.x, self.y = position
        self.w, self.h = size
        self.through = through
        self.animation = animation

        self.texts: list[Text] = []
        self.shapes: list[Shape] = []
        self.images: list[Image] = []

        self.feature: Feature = None

        self.state: State = state

        master._widgets.append(self)

    def register(self, component: Component) -> None:
        """"""
        if isinstance(component, Shape):
            self.shapes.append(component)
        elif isinstance(component, Text):
            self.texts.append(component)
        elif isinstance(component, Image):
            self.images.append(component)
        else:
            raise TypeError
        component.display()
        component.update(no_delay=True)

    def _zoom(self, ratio: tuple[float, float] | None = None) -> None:
        """Zoom self"""
        if ratio is None:
            ratio = self.master._ratio
        self.w *= ratio[0]
        self.h *= ratio[1]
        self.x *= ratio[0]
        self.y *= ratio[1]
        for elem in self.shapes + self.texts + self.images:
            elem.zoom(ratio)

    def update(self, state: State | None = None, *, no_delay: bool = False) -> None:
        """Update the widget"""
        if state is not None:
            self.state = state
        for elem in self.shapes + self.texts:
            elem.update(state, no_delay=no_delay)

    def move(self, dx: int, dy: int) -> None:
        """Move the widget"""
        self.x += dx
        self.y += dy
        for elem in self.shapes + self.texts + self.images:
            elem.move(dx, dy)

    def moveto(self, x: int, y: int) -> None:
        """Move the Widget to a certain position"""
        return self.move(x - self.x, y - self.y)

    def destroy(self) -> None:
        """Destroy the widget"""
        self.master._widgets.remove(self)
        for elem in self.shapes + self.texts + self.images:
            elem.destroy()

    def focus_set(self, *args) -> None:
        """"""
        self.master.focus(*args)
