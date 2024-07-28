"""All containers"""

import functools
import math
import platform
import tkinter
import tkinter.font
import typing

from ..style import manager, parser
from ..toolbox import enhanced, tools
from . import constants, virtual

__all__ = [
    "Tk",
    "Toplevel",
    "Canvas",
    "Frame",
]


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
        **kwargs,
    ) -> None:
        """
        * `size`: the size of the window, default value is 1280x720(px)
        * `position`: the position of the window, default value indicates that the location is random
        * `title`: the title of the window, default value is an empty string
        * `**kwargs`: compatible with other parameters of class `tkinter.Tk`
        """
        if not isinstance(self, Toplevel):  # tkt.Toplevel and its subclasses do not inherit tk.Tk
            tkinter.Tk.__init__(self, **kwargs)

        self._size = self._initial_size = tuple(size)
        self._canvases: list[Canvas] = []

        self.title(title)
        self.geometry(size=size, position=position)
        self._theme(manager.get_color_mode() == "dark",
                    include_children=False, include_canvases=False)
        manager.register_event(self._theme)
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

        TIPS:

        If you want to use `tkinter.Tk.geometry`, please use `tkinter.Tk.wm_geometry` instead

        CAUTION:

        This method causes the event `<configure>` to be triggered
        """
        if size is not None and position is not None:
            self.wm_geometry(
                f"{size[0]}x{size[1]}+{position[0]}+{position[1]}")
        elif size is not None:
            self.wm_geometry(f"{size[0]}x{size[1]}")
        elif position is not None:
            self.wm_geometry(f"+{position[0]}+{position[1]}")
        return *self._size, self.winfo_x(), self.winfo_y()

    @property
    def canvases(self) -> tuple["Canvas", ...]:
        """Retrun all instances of `Canvas` of the widget"""
        return tuple(self._canvases)

    @functools.cached_property
    def ratios(self) -> tuple[float, float]:
        """Return the aspect zoom ratio of the widget"""
        return tuple(i/j for i, j in zip(self._size, self._initial_size))

    def _zoom(self) -> None:
        """Zoom contents of the window"""
        new_size = self.winfo_width(), self.winfo_height()
        if self._size != new_size:
            self._size = new_size  # Update the current size

            if self.__dict__.get("ratios"):
                del self.__dict__["ratios"]  # Clear cache to update ratios

            for canvas in self._canvases:
                canvas._re_place()

    def _theme(
        self,
        dark: bool,
        *,
        include_children: bool = True,
        include_canvases: bool = True,
    ) -> None:
        """
        Change the color theme of the window

        * `dark`: whether it is in dark mode
        * `include_children`: wether include its children, like Toplevel
        * `include_canvases`: wether include its canvases
        """
        self.update_idletasks()
        self["bg"] = "#202020" if dark else "#F1F1F1"
        manager.customize_window(self, style="dark" if dark else "normal")
        if include_children:
            for child in self.children:
                if isinstance(child, Toplevel):
                    child._theme(dark, include_canvases=include_canvases)
        if include_canvases:
            for canvas in self._canvases:
                canvas._theme(dark)

    def center(self, master: tkinter.Misc | None = None) -> None:
        """
        Center the widget

        `master`: The area of the reference widget, if it is None,
        means that the reference area is the entire screen
        """
        if master is None:  # center self in whole screen
            parent_width = self.winfo_screenwidth()
            parent_height = self.winfo_screenheight()
            dx, dy = 0, 0
        else:
            parent_width = master.winfo_width()
            parent_height = master.winfo_height()
            dx, dy = master.winfo_x(), master.winfo_y()

        x = (parent_width - self._size[0]) // 2
        y = (parent_height - self._size[1]) // 2
        self.geometry(position=(x + dx, y + dy))

    def alpha(self, value: float | None = None) -> float | None:
        """
        Set or get the transparency of the window

        * `value`: the transparency of the window, range is 0~1
        """
        if (result := self.attributes("-alpha", value)) is None:
            return result
        return bool(result)

    def topmost(self, value: bool | None = True) -> bool | None:
        """
        Set or get whether the window is pinned or not

        * `value`: indicate whether the window is topmost
        """
        if (result := self.attributes("-topmost", value)) is None:
            return result
        return bool(result)

    def fullscreen(self, value: bool | None = True) -> bool | None:
        """
        Set or get whether the window is full-screen

        * `value`: indicate whether the window is full-screen

        TIPS:

        The method should be called at the end of the code,
        or after some time after the program has started
        """
        if (result := self.attributes("-fullscreen", value)) is not None:
            return self._theme(manager.get_color_mode() == "dark", include_canvases=False)
        return result

    def toolwindow(self, value: bool | None = True) -> bool | None:
        """
        Set or get whether the window is tool-window

        * `value`: indicate whether the window is tool-window
        """
        if (result := self.attributes("-toolwindow", value)) is not None:
            return self._theme(manager.get_color_mode() == "dark", include_children=False, include_canvases=False)
        return result

    def transparentcolor(self, value: str | None = None) -> str | None:
        """
        Set or get the penetration color of the window

        * `value`: the penetration color of the window
        """
        return self.attributes("-transparentcolor", value)

    def shutdown(self, command: typing.Callable | None, *args, **kwargs) -> None:
        """
        Set a function that will be called when the window is closed

        * `command`: the function that was called
        * `args`: the variable-length argument of the called function
        * `kwargs`: the keyword argument of the function being called

        TIPS:

        Regardless of whether the function is successfully called or not,
        the window will still close gracefully
        """
        def _wrapper() -> None:
            """Ensure that the window closes gracefully"""
            try:
                command(*args, **kwargs)
            finally:
                self.destroy()

        self.protocol("WM_DELETE_WINDOW", _wrapper)


class Toplevel(tkinter.Toplevel, Tk):
    """
    Toplevel window

    It can be used as a pop-up window,
    or it can be customized to put anything you want to show in it
    """

    def __init__(
        self,
        master: Tk | None = None,
        size: tuple[int, int] = (960, 540),
        position: tuple[int, int] | None = None,
        *,
        title: str | None = None,
        transient: bool = False,
        grab: bool = False,
        focus: bool = True,
        **kwargs,
    ) -> None:
        """
        * `master`: parent widget
        * `size`: the size of the window, default value is 960x540(px)
        * `position`: the position of the window, default value indicates that the location is random
        * `title`: title of window, default is the same as title of master
        * `transient`: instruct the window manager that this window is transient with regard to its master
        * `grab`: set grab for this window
        * `focus`: whether direct input focus to this window
        * `**kwargs`: compatible with other parameters of class `tkinter.Toplevel`
        """
        tkinter.Toplevel.__init__(self, master, **kwargs)

        if transient:
            self.transient(self.master)

        Tk.__init__(self, size, position, title=title)  # window style is set

        if grab:
            self.grab_set()
        if focus:
            self.focus_set()

    # @typing.override
    def destroy(self) -> None:
        manager.remove_event(self._theme)
        return tkinter.Toplevel.destroy(self)


class Canvas(tkinter.Canvas):
    """
    Scalable Canvas

    The parent widget of all virtual widgets of tkintertools is `Canvas`
    """

    def __init__(
        self,
        master: "Tk | Canvas",
        *,
        expand: typing.Literal["", "x", "y", "xy"] = "xy",
        zoom_item: bool = False,
        keep_ratio: typing.Literal["min", "max"] | None = None,
        free_anchor: bool = False,
        name: str | None = None,
        **kwargs,
    ) -> None:
        """
        * `master`: parent widget
        * `expand`: the mode of expand, `x` is horizontal, and `y` is vertical
        * `zoom_item`: whether or not to scale its items
        * `keep_ratio`: the mode of aspect ratio, `min` follows the minimum value, `max` follows the maximum value
        * `free_anchor`: whether the anchor point is free-floating
        * `kwargs`: compatible with other parameters of class `tkinter.Canvas`
        """
        tkinter.Canvas.__init__(self, master, **kwargs)

        # The following four attributes are not initialized yet, only types are defined,
        # and they are initialized when method `self._initialization` is called.
        # Once the attribute self._initial_* is assigned, it should not be modified again

        self._initial_size: tuple[int, int]
        self._initial_position: tuple[int, int]
        self._size: tuple[int, int]
        self._position: tuple[int, int]

        self._canvases: list[Canvas] = []
        self._widgets: list[virtual.Widget] = []
        self._items: list[int] = []
        self._images: dict[int, list[enhanced.PhotoImage]] = {}
        # initial image, now image

        self.name = name

        self.master: Tk | Canvas  # Coverred original type hint

        self._expand: typing.Literal["", "x", "y", "xy"] = expand
        self._zoom_item = zoom_item
        self._free_anchor = free_anchor
        self._keep_ratio: typing.Literal["min", "max"] | None = keep_ratio

        self._trigger_config = tools._Trigger(
            lambda **kwargs: self.configure(**{k: v for k, v in kwargs.items() if self[k] != v}))
        self._trigger_focus = tools._Trigger(self.focus)

        self._theme(manager.get_color_mode() == "dark")

        master._canvases.append(self)

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

        self.bind("<<Copy>>", self._copy)
        self.bind("<<Paste>>", self._paste)
        self.bind("<<Cut>>", self._cut)

        self.bind("<Configure>", lambda _: self._zoom_self())

    @property
    def canvases(self) -> tuple["Canvas", ...]:
        """Retrun all child `Canvas` of the `Canvas`"""
        return tuple(self._canvases)

    @property
    def widgets(self) -> tuple[virtual.Widget, ...]:
        """Retrun all `Widget` of the `Canvas`"""
        return tuple(self._widgets)

    @property
    def items(self) -> tuple[int, ...]:
        """Retrun all items of the `Canvas`"""
        return tuple(self._items)

    @property
    def images(self) -> tuple[int, ...]:
        """Retrun all images of the `Canvas`"""
        return tuple(self._images)

    @functools.cached_property
    def ratios(self) -> tuple[float, float]:
        """Return the aspect zoom ratio of the widget"""
        return tuple(i/j for i, j in zip(self._size, self._initial_size))

    def _theme(self, dark: bool) -> None:
        """
        Change the color theme of the Canvas and its items

        * `dark`: whether it is in dark mode
        """
        self.update_idletasks()
        self.configure(**parser.get(self))
        for widget in self._widgets:
            for component in widget._shapes + widget._texts + widget._images:
                if styles := parser.get(widget, component):
                    component.styles = styles
            if widget._state_before_disabled:
                widget.disabled()
            else:
                widget.update()
        for canvas in self._canvases:
            canvas._theme(dark)

    def _initialization(self) -> None:
        """Initialization of size data"""
        self._size = self._initial_size = self.winfo_width(), self.winfo_height()

        match self.place_info().get("anchor"):
            case "nw" | None: dx, dy = 0, 0
            case "n": dx, dy = self._initial_size[0]//2, 0
            case "w": dx, dy = 0, self._initial_size[1]//2
            case "ne": dx, dy = self._initial_size[0], 0
            case "sw": dx, dy = 0, self._initial_size[1]
            case "e": dx, dy = self._initial_size[0], self._initial_size[1]//2
            case "s": dx, dy = self._initial_size[0], self._initial_size[1]//2
            case "se": dx, dy = self._initial_size[0], self._initial_size[1]
            case "center": dx, dy = self._initial_size[0]//2, self._initial_size[1]//2
            # The above is already all the case

        self._position = self._initial_position = self.winfo_x()+dx, self.winfo_y()+dy

    def _re_place(self) -> None:
        """
        Resize and position the `Canvas` based on the relevant parameters

        WARNING:

        This method only works for Canvas with Place layout
        """
        if self.winfo_viewable() and self.place_info():
            match self._keep_ratio:
                case "max": ratio_x = ratio_y = max(self.master.ratios)
                case "min": ratio_x = ratio_y = min(self.master.ratios)
                case None: ratio_x, ratio_y = self.master.ratios

            kwargs: dict[str, float] = {}

            if "x" in self._expand:
                kwargs["width"] = self._initial_size[0]*ratio_x
            if "y" in self._expand:
                kwargs["height"] = self._initial_size[1]*ratio_y
            if self._free_anchor:
                kwargs["x"] = self._initial_position[0]*self.master.ratios[0]
                kwargs["y"] = self._initial_position[1]*self.master.ratios[1]

            if kwargs:
                self.place(**kwargs)

    def _zoom_self(self) -> None:
        """Scale the `Canvas` itself"""
        if not hasattr(self, "_size"):
            return self._initialization()

        last_size = self._size[:]  # temporary value
        self._position = self.winfo_x(), self.winfo_y()
        self._size = self.winfo_width(), self.winfo_height()

        if self.__dict__.get("ratios"):
            del self.__dict__["ratios"]  # Clear cache to update the ratios

        if self._zoom_item:
            relative_ratio = tuple(i/j for i, j in zip(self._size, last_size))
            self._zoom_children(relative_ratio)
            for widget in self._widgets:
                widget.zoom(relative_ratio)

        for canvas in self._canvases:
            canvas._re_place()

    def _zoom_children(self, relative_ratio: tuple[float, float]) -> None:
        """Experimental: Scale the tkinter Widgets"""
        for tk_widgets in tuple(self.children.values()):
            if tk_widgets in self.canvases:
                continue
            if tk_widgets.place_info():
                width = tk_widgets.winfo_width()*relative_ratio[0]
                height = tk_widgets.winfo_height()*relative_ratio[1]
                x = tk_widgets.winfo_x()*relative_ratio[0]
                y = tk_widgets.winfo_y()*relative_ratio[1]
                tk_widgets.place(width=width, height=height, x=x, y=y)

    # @typing.override
    def destroy(self) -> None:
        self.master._canvases.remove(self)
        return tkinter.Canvas.destroy(self)

    # @typing.override
    def create_text(self, x: float, y: float, /, **kwargs) -> int:
        # XXX: Need to be improved
        if not (font_ := kwargs.get("font")):
            kwargs["font"] = tkinter.font.Font(
                family=constants.FONT, size=constants.SIZE)
        elif isinstance(font_, str):
            kwargs["font"] = tkinter.font.Font(
                family=font_, size=constants.SIZE)
        elif isinstance(font_, int):
            kwargs["font"] = tkinter.font.Font(
                family=constants.FONT, size=-abs(font_))
        elif isinstance(font_, tkinter.font.Font):
            kwargs["font"].config(size=-abs(font_.cget("size")))
        else:
            (font_ := list(font_))[1] = -abs(font_[1])
            length = len(font_)
            kwargs["font"] = tkinter.font.Font(
                family=font_[0], size=font_[1],
                weight=font_[2] if length > 2 else "normal",
                slant=font_[3] if length > 3 else "roman")

        return tkinter.Canvas.create_text(self, x, y, **kwargs)

    def _move(
        self,
        event: tkinter.Event,
        type_: typing.Literal["left", "center", "right", "none"]
    ) -> None:
        """Internal Method: Events to move the mouse"""
        self._trigger_config.reset()
        for widget in self._widgets[::-1]:
            if widget._feature is not None:
                if getattr(widget._feature, f"_move_{type_}")(event) and not widget.through:
                    event.x = math.nan
        self._trigger_config.update(cursor="arrow")

    def _click(
        self,
        event: tkinter.Event,
        type_: typing.Literal["left", "center", "right"]
    ) -> None:
        """Events to active the mouse"""
        self.focus_set()
        self._trigger_focus.reset()
        for widget in self._widgets[::-1]:
            if widget._feature is not None:
                if getattr(widget._feature, f"_click_{type_}")(event) and not widget.through:
                    event.x = math.nan
        self._trigger_focus.update(True, "")

    def _release(
        self,
        event: tkinter.Event,
        type_: typing.Literal["left", "center", "right"]
    ) -> None:
        """Events to release the mouse"""
        for widget in self._widgets[::-1]:
            if widget._feature is not None:
                if getattr(widget._feature, f"_release_{type_}")(event) and not widget.through:
                    event.x = math.nan

    def _wheel(
        self,
        event: tkinter.Event,
        type_: typing.Literal["up", "down"] | None = None
    ) -> None:
        """Events to scroll the mouse wheel"""
        if type_ is not None:
            event.delta = 120 if type_ == "up" else -120
        for widget in self._widgets[::-1]:
            if widget._feature is not None:
                if getattr(widget._feature, "_wheel")(event) and not widget.through:
                    event.x = math.nan

    def _input(self, event: tkinter.Event) -> None:
        """Event for typing"""
        for widget in self._widgets[::-1]:
            if widget._feature is not None:
                if getattr(widget._feature, "_input")(event) and not widget.through:
                    event.x = math.nan

    def _copy(self, event: tkinter.Event) -> None:
        """Event for copy operation"""
        for widget in self._widgets[::-1]:
            if widget._feature is not None:
                if getattr(widget._feature, "_copy")(event) and not widget.through:
                    pass

    def _paste(self, event: tkinter.Event) -> None:
        """Event for paste operation"""
        for widget in self._widgets[::-1]:
            if widget._feature is not None:
                if getattr(widget._feature, "_paste")(event) and not widget.through:
                    pass

    def _cut(self, event: tkinter.Event) -> None:
        """Event for cut operation"""
        for widget in self._widgets[::-1]:
            if widget._feature is not None:
                if getattr(widget._feature, "_cut")(event) and not widget.through:
                    pass


class Frame(Canvas):
    """A frame for auxiliary layouts"""

    def __init__(
        self,
        master: "Tk | Canvas | Frame",
        *,
        expand: typing.Literal["", "x", "y", "xy"] = "xy",
        zoom_item: bool = False,
        keep_ratio: typing.Literal["min", "max"] | None = None,
        free_anchor: bool = False,
        name: str | None = None,
        **kwargs,
    ) -> None:
        """
        * `master`: parent widget
        * `expand`: the mode of expand, `x` is horizontal, and `y` is vertical
        * `zoom_item`: whether or not to scale its items
        * `keep_ratio`: the mode of aspect ratio, `min` follows the minimum value, `max` follows the maximum value
        * `free_anchor`: whether the anchor point is free-floating
        * `kwargs`: compatible with other parameters of class `tkinter.Canvas`
        """
        Canvas.__init__(self, master, expand=expand, zoom_item=zoom_item,
                        keep_ratio=keep_ratio, free_anchor=free_anchor, name=name, **kwargs)
