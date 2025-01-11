"""All containers.

There are two containers at the window level: `Tk` and `Toplevel`. `Tk` is
generally used for the main window, while `Toplevel` is a pop-up window.

There is another container at the canvas level: `Canvas`. `Canvas` is the main
container carrier.
"""

from __future__ import annotations

__all__ = [
    "Tk",
    "Toplevel",
    "Canvas",
]

import abc
import collections.abc
import functools
import platform
import tkinter
import tkinter.font
import traceback
import typing

import typing_extensions

from ..theme import manager
from ..toolbox import enhanced, utility
from . import configs, virtual


class Misc(abc.ABC):
    """An abstract miscellaneous class that implements some details.

    Currently, this class implements the ability to use the `with` statement
    for its subclasses for testing.
    """

    @abc.abstractmethod
    def destroy(self) -> None:
        """Destroy the object."""

    def __enter__(self) -> typing_extensions.Self:
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.destroy()


class Tk(tkinter.Tk, Misc):
    """Main window.

    In general, there is only one main window. But after destroying it, another
    one can be created.
    """

    light = {"bg": "#F1F1F1"}
    dark = {"bg": "#202020"}

    def __init__(
        self,
        size: tuple[int, int] = (1280, 720),
        position: tuple[int, int] | None = None,
        *,
        title: str | None = None,
        icon: str | enhanced.PhotoImage | None = None,
        **kwargs,
    ) -> None:
        """
        * `size`: size of the window
        * `position`: position of the window, based on the upper left (nw)
        corner. And negative numbers are based on the bottom right (se) corner.
        * `title`: title of the window, default value is `"tk"`
        * `icon`: icon of the window, default value is the icon of tk
        * `**kwargs`: compatible with other parameters of class `tkinter.Tk`
        """
        if not isinstance(self, Toplevel):
            # containers.Toplevel and its subclasses do not inherit tk.Tk
            tkinter.Tk.__init__(self, **kwargs)

        # ensure init_size is a tuple
        self.init_size: typing.Final[tuple[int, int]] = size[0], size[1]
        self.canvases: list[Canvas] = []
        self.size = self.init_size

        self.light, self.dark = self.light.copy(), self.dark.copy()

        self.update()  # wm_iconbitmap will not take effect without this line

        self._icon: str | enhanced.PhotoImage | None = icon

        if icon is not None:
            self.icon(icon)

        if title is not None:
            self.wm_title(title)

        self.geometry(size=size, position=position)

        self.theme(
            manager.get_color_mode(), include_children=False,
            include_canvases=False)
        manager.register_event(self.theme)

        for name in "transient", "resizable", "overrideredirect":
            self._wrap_method(name)

        self.bind("<Configure>", lambda _: self._zoom())

    @functools.cached_property
    def ratios(self) -> tuple[float, float]:
        """Return the aspect zoom ratio of the container."""
        return self.size[0]/self.init_size[0], self.size[1]/self.init_size[1]

    @staticmethod
    def _fixed_theme(method) -> collections.abc.Callable:
        """This is a decorator that to fix a problem that some methods cause
        the window to lose its theme.

        * `method`: the method of being decorated
        """
        @functools.wraps(method)
        def wrapper(tk: Tk, *args, **kwargs) -> typing.Any:
            result = method(tk, *args, **kwargs)

            if result is None:
                tk.theme(
                    manager.get_color_mode(),
                    include_children=False, include_canvases=False)

            return result

        return wrapper

    def _wrap_method(self, method_name: str) -> None:
        """Some problems can be fixed by decorating the original method.

        * `method_name`: the name of the method to be decorated
        """
        method = getattr(tkinter.Wm, method_name)

        @Tk._fixed_theme
        @functools.wraps(method)
        def wrapper(*args, **kwargs) -> typing.Any:
            result = method(*args, **kwargs)

            return None if result == "" else result

        setattr(self, method_name,
                lambda *args, **kwargs: wrapper(self, *args, **kwargs))

    def _zoom(self) -> None:
        """Zoom contents of the window."""
        # Using tkinter.Event here will result in incorrect results
        new_size = self.winfo_width(), self.winfo_height()

        if self.size == new_size:
            return

        self.size = new_size  # Update the current size

        if self.__dict__.get("ratios"):
            del self.__dict__["ratios"]  # Clear cache to update ratios

        for canvas in self.canvases:
            canvas.zoom()

    def theme(
        self,
        value: typing.Literal["light", "dark"],
        *,
        include_children: bool = True,
        include_canvases: bool = True,
    ) -> None:
        """Change the color theme of the window

        * `value`: theme name
        * `include_children`: wether include its children, like Toplevel
        * `include_canvases`: wether include its canvases
        """
        self.update()
        self.configure(bg=getattr(self, value)["bg"])
        manager.apply_theme(self, theme="dark" if value == "dark" else "normal")

        if include_children:
            for child in self.children.values():
                if isinstance(child, Toplevel):
                    child.theme(value, include_canvases=include_canvases,
                                include_children=include_children)

        if include_canvases:
            for canvas in self.canvases:
                if canvas.auto_update:
                    canvas.theme(value)

    def geometry(
        self,
        *,
        size: tuple[int, int] | None = None,
        position: tuple[int, int] | None = None
    ) -> tuple[int, int, int, int] | None:
        """Change the size and position of the window and return the current
        size and position of the window.

        * `size`: the size of the window, if it is None, does not change anything
        * `position`: the position of the window, if it is None, does not change anything

        If you want to use `tkinter.Tk.geometry`, please use
        `tkinter.Tk.wm_geometry` instead.
        """
        if size is not None and position is not None:
            self.wm_geometry(f"{size[0]}x{size[1]}+{position[0]}+{position[1]}")
        elif size is not None:
            self.wm_geometry(f"{size[0]}x{size[1]}")
        elif position is not None:
            self.wm_geometry(f"+{position[0]}+{position[1]}")

        return *self.size, self.winfo_x(), self.winfo_y()

    def center(self, *, refer: tkinter.Misc | None = None) -> None:
        """Center the container

        `refer`: The area of the reference widget, if it is None, means that
        the reference area is the entire screen.
        """
        if refer is None:  # center self in whole screen
            w, h = self.winfo_screenwidth(), self.winfo_screenheight()
            dx, dy = 0, 0
        else:
            w, h = refer.winfo_width(), refer.winfo_height()
            dx, dy = refer.winfo_x(), refer.winfo_y()

        x, y = (w-self.size[0]) // 2, (h-self.size[1]) // 2
        self.geometry(position=(x+dx, y+dy))

    def icon(self, value: str | enhanced.PhotoImage) -> None:
        """Set the icon of the window.

        * `value`: the icon
        """
        self._icon = value

        if isinstance(value, enhanced.PhotoImage):
            self.wm_iconphoto(False, value)
        elif isinstance(value, str):
            if value:
                self.wm_iconbitmap(value)
            elif platform.system() == "Windows" and isinstance(self, Tk):
                # now, the value is ""
                self.call("wm", "iconbitmap", self, "-default", value)

    def alpha(self, value: float | None = None) -> float | None:
        """Set or get the transparency of the window

        * `value`: the transparency of the window, range is 0~1
        """
        result = self.wm_attributes("-alpha", value)
        return None if result == "" else result

    def topmost(self, value: bool | None = True) -> bool | None:
        """Set or get whether the window is pinned or not

        * `value`: indicate whether the window is topmost
        """
        result = self.wm_attributes("-topmost", value)
        return None if result == "" else bool(result)

    @_fixed_theme
    def fullscreen(self, value: bool | None = True) -> bool | None:
        """Set or get whether the window is full-screen.

        * `value`: indicate whether the window is full-screen

        The method should be called at the end of the code, or after some time
        after the program has started.
        """
        if value is False and platform.system() == "Darwin":  # patch for Darwin
            value = not self.fullscreen(None)

        result = self.wm_attributes("-fullscreen", value)
        return None if result == "" else bool(result)

    if platform.system() == "Windows":

        @_fixed_theme
        def toolwindow(self, value: bool | None = True) -> bool | None:
            """Set or get whether the window is tool-window

            * `value`: indicate whether the window is tool-window

            This method only works on Windows!
            """
            result = self.wm_attributes("-toolwindow", value)
            return None if result == "" else bool(result)

        def transparentcolor(self, value: str | None = None) -> str | None:
            """Set or get the penetration color of the window

            * `value`: the penetration color of the window

            This method only works on Windows!
            """
            result = self.wm_attributes("-transparentcolor", value)
            return None if result == "" else result

    @typing_extensions.override
    def destroy(self) -> None:
        """Destroy this and all descendants widgets."""
        manager.remove_event(self.theme)
        return tkinter.Tk.destroy(self)

    def at_exit(
        self,
        command: collections.abc.Callable[[], typing.Any],
        *,
        ensure_destroy: bool = True,
    ) -> None:
        """Set a function that will be called when the window is closed.

        * `command`: the function that was called
        * `ensure_destroy`: whether the window is guaranteed to be closed
        """
        def wrapper() -> None:
            try:
                command()
            except Exception as exc:  # pylint: disable=W0718
                traceback.print_exception(exc)
            finally:
                if ensure_destroy:
                    self.destroy()

        self.wm_protocol("WM_DELETE_WINDOW", wrapper)


class Toplevel(tkinter.Toplevel, Tk, Misc):
    """Toplevel window.

    It can be used as a pop-up window, or it can be customized to put anything
    you want to show.
    """

    def __init__(
        self,
        master: Tk | Toplevel | None = None,
        size: tuple[int, int] = (960, 540),
        position: tuple[int, int] | None = None,
        *,
        title: str | None = None,
        icon: str | enhanced.PhotoImage | None = None,
        grab: bool = False,
        focus: bool = True,
        **kwargs,
    ) -> None:
        """
        * `master`: parent widget
        * `size`: size of the window, default value is 960x540(px)
        * `position`: position of the window, default value indicates random
        * `title`: title of window, default is the same as title of master
        * `icon`: icon of the window, default is the same as title of master
        * `grab`: set grab for this window
        * `focus`: whether direct input focus to this window
        * `**kwargs`: compatible with other parameters of class `tkinter.Toplevel`
        """
        tkinter.Toplevel.__init__(self, master, **kwargs)

        if icon is None:
            icon = getattr(self.master, "_icon", None)  # For some rare cases

        Tk.__init__(self, size, position, title=title, icon=icon)  # set style

        if grab:
            self.grab_set()

        if focus:
            self.focus_set()

    @typing_extensions.override
    def destroy(self) -> None:
        """Destroy this and all descendants widgets."""
        manager.remove_event(self.theme)
        return tkinter.Toplevel.destroy(self)


class Canvas(tkinter.Canvas, Misc):
    """Main contrainer: Canvas.

    The parent widget of all virtual widgets is `Canvas`.
    """

    light = {
        "bg": "#F1F1F1",
        "insertbackground": "#000000",
        "highlightthickness": 0,
        "selectborderwidth": 0,
    }

    dark = {
        "bg": "#202020",
        "insertbackground": "#FFFFFF",
        "highlightthickness": 0,
        "selectborderwidth": 0,
    }

    def __init__(
        self,
        master: Tk | Toplevel | Canvas | None = None,
        *,
        expand: typing.Literal["", "x", "y", "xy"] = "xy",
        auto_zoom: bool = False,
        keep_ratio: typing.Literal["min", "max"] | None = None,
        free_anchor: bool = False,
        auto_update: bool | None = None,
        zoom_all_items: bool = False,
        **kwargs,
    ) -> None:
        """
        * `master`: parent widget
        * `expand`: the mode of expand, `x` is horizontal, and `y` is vertical
        * `auto_zoom`: whether or not to scale its items automatically
        * `keep_ratio`: the mode of aspect ratio, `min` follows the minimum
        value, `max` follows the maximum value
        * `free_anchor`: whether the anchor point is free-floating
        * `auto_update`: whether the theme manager update it automatically
        * `zoom_all_items`: (Experimental) whether or not to scale its all items
        * `kwargs`: compatible with other parameters of class `tkinter.Canvas`
        """
        tkinter.Canvas.__init__(self, master, **kwargs)

        self.master: Tk | Toplevel | Canvas  # just for type hint

        # The following four attributes are not initialized yet, only types are
        # defined, and they are initialized when method `self._initialization`
        # is called. Once the attribute self._init_* is assigned, it should not
        # be modified again.

        self.init_size: tuple[int, int]
        self.init_position: tuple[int, int]

        self._size: tuple[int, int]
        self._position: tuple[int, int]

        self.canvases: list[Canvas] = []
        self.widgets: list[virtual.Widget] = []

        self.events: list[str] = []

        if auto_update is None:
            self.auto_update = configs.Env.auto_update
        else:
            self.auto_update = auto_update

        self._expand: typing.Literal["", "x", "y", "xy"] = expand
        self._auto_zoom = auto_zoom
        self._free_anchor = free_anchor
        self._keep_ratio: typing.Literal["min", "max"] | None = keep_ratio
        self._zoom_all_items = zoom_all_items

        self.trigger_focus = utility.Trigger(self.focus)
        self.trigger_config = utility.Trigger(lambda **kwargs: self.configure(
            **{k: v for k, v in kwargs.items() if self[k] != v}))

        if self.auto_update:
            self.theme(manager.get_color_mode())

        self.light, self.dark = self.light.copy(), self.dark.copy()

        self.master.canvases.append(self)

        self.bind("<KeyPress>", self.on_key_press)
        self.bind("<KeyRelease>", self.on_key_release)
        self.bind("<MouseWheel>", lambda event: self.on_wheel(event, None))
        self.bind("<Button-4>", lambda event: self.on_wheel(event, True))
        self.bind("<Button-5>", lambda event: self.on_wheel(event, False))

        for _n in "<Button-1>", "<Button-2>", "<Button-3>":
            self.bind(_n, lambda e, n=_n: self.on_click(e, n))

        for _n in "<Motion>", "<B1-Motion>", "<B2-Motion>", "<B3-Motion>":
            self.bind(_n, lambda e, n=_n: self.on_motion(e, n))

        for _n in "<ButtonRelease-1>", "<ButtonRelease-2>", "<ButtonRelease-3>":
            self.bind(_n, lambda e, n=_n: self.on_release(e, n))

        for _n in configs.Constant.PREDEFINED_VIRTUAL_EVENTS:
            self.register_event(_n)

        self.bind("<Configure>", lambda _: self._zoom_self())

    @functools.cached_property
    def ratios(self) -> tuple[float, float]:
        """Return the aspect zoom ratio of the widget."""
        return self._size[0]/self.init_size[0], self._size[1]/self.init_size[1]

    def theme(self, value: typing.Literal["light", "dark"]) -> None:
        """Change the color theme of the Canvas and its items

        * `value`: theme name
        """
        self.update()
        self.configure(getattr(self, manager.get_color_mode(), {}))

        for widget in self.widgets:
            if widget.style.auto_update:
                if widget.state_before_disabled:
                    widget.disable()
                else:
                    widget.update()

        for canvas in self.canvases:
            canvas.theme(value)

    def _initialization(self) -> None:
        """Initialization of size data."""
        self.init_size = self.winfo_width(), self.winfo_height()
        self._size = self.init_size

        match self.place_info().get("anchor", "nw"):
            case "nw": dx, dy = 0, 0
            case "n": dx, dy = self.init_size[0]//2, 0
            case "w": dx, dy = 0, self.init_size[1]//2
            case "ne": dx, dy = self.init_size[0], 0
            case "sw": dx, dy = 0, self.init_size[1]
            case "e": dx, dy = self.init_size[0], self.init_size[1]//2
            case "s": dx, dy = self.init_size[0], self.init_size[1]//2
            case "se": dx, dy = self.init_size[0], self.init_size[1]
            case "center": dx, dy = self.init_size[0]//2, self.init_size[1]//2

        self.init_position = self.winfo_x() + dx, self.winfo_y() + dy
        self._position = self.init_position

    def zoom(self) -> None:
        """Resize and position the `Canvas` based on the relevant parameters.

        This method only works for Canvas with Place layout.
        """
        if self.winfo_viewable() and self.place_info():
            match self._keep_ratio:
                case "max": ratio_x = ratio_y = max(self.master.ratios)
                case "min": ratio_x = ratio_y = min(self.master.ratios)
                case None: ratio_x, ratio_y = self.master.ratios

            kwargs: dict[str, float] = {}

            if "x" in self._expand:
                kwargs["width"] = self.init_size[0]*ratio_x
            if "y" in self._expand:
                kwargs["height"] = self.init_size[1]*ratio_y
            if self._free_anchor:
                kwargs["x"] = self.init_position[0]*self.master.ratios[0]
                kwargs["y"] = self.init_position[1]*self.master.ratios[1]

            if kwargs:
                self.place(kwargs)

    def _zoom_self(self) -> None:
        """Scale the `Canvas` itself."""
        if not hasattr(self, "_size"):
            self._initialization()
            return

        size = self._size  # temporary value
        self._position = self.winfo_x(), self.winfo_y()
        self._size = self.winfo_width(), self.winfo_height()

        if self.__dict__.get("ratios"):
            del self.__dict__["ratios"]  # Clear cache to update the ratios

        if self._auto_zoom:
            relative_ratio = self._size[0]/size[0], self._size[1]/size[1]
            self._zoom_tk_widgets(relative_ratio)

            for widget in self.widgets:
                # Nested widget will be zoomed by its parent widget
                if not widget.nested:
                    widget.zoom(relative_ratio)

            if self._zoom_all_items:
                for item in self.find_all():
                    if self.gettags(item):
                        continue
                    self.scale(item, 0, 0, relative_ratio[0], relative_ratio[1])

        for canvas in self.canvases:
            canvas.zoom()

    def _zoom_tk_widgets(self, rel_ratio: tuple[float, float]) -> None:
        """Scale the tkinter widgets of the Canvas.

        * `rel_ratio`: the ratio of the current size to the previous size
        """
        for tk_widgets in tuple(self.children.values()):
            if tk_widgets in self.canvases:
                continue
            if tk_widgets.place_info():
                width = tk_widgets.winfo_width()*rel_ratio[0]
                height = tk_widgets.winfo_height()*rel_ratio[1]
                x = tk_widgets.winfo_x()*rel_ratio[0]
                y = tk_widgets.winfo_y()*rel_ratio[1]
                tk_widgets.place(width=width, height=height, x=x, y=y)

    @typing_extensions.override
    def destroy(self) -> None:
        """Destroy this and all descendants widgets."""
        self.master.canvases.remove(self)

        for widget in tuple(self.widgets):
            # Nested widget will be destroyed by its parent widget
            if not widget.nested:
                widget.destroy()

        return tkinter.Canvas.destroy(self)

    def clear(self) -> None:
        """Clear all things in the Canvas."""
        self.canvases.clear()
        self.widgets.clear()

        for child in tuple(self.children.values()):
            child.destroy()

        self.delete(*self.find_all())

    @typing_extensions.override
    def create_text(self, x: float, y: float, /, *args, **kwargs) -> int:
        """Create text with coordinates x, y."""
        font = kwargs.get("font")
        if not font:
            kwargs["font"] = tkinter.font.Font(
                family=configs.Font.family, size=configs.Font.size)
        elif isinstance(font, str):
            kwargs["font"] = tkinter.font.Font(
                family=font, size=configs.Font.size)
        elif isinstance(font, int):
            kwargs["font"] = tkinter.font.Font(
                family=configs.Font.family, size=-abs(font))
        elif isinstance(font, tkinter.font.Font):
            kwargs["font"].config(size=-abs(font.cget("size")))
        else:
            kwargs["font"] = tkinter.font.Font(
                family=font[0], size=-abs(font[1]),
                weight=font[2] if len(font) > 2 else "normal",
                slant=font[3] if len(font) > 3 else "roman")

        return tkinter.Canvas.create_text(self, x, y, *args, **kwargs)

    def on_motion(self, event: tkinter.Event, name: str) -> None:
        """Events to move the mouse"""
        self.trigger_config.reset()
        for widget in self.widgets[::-1]:
            if hasattr(widget, "feature") and not widget.disappeared:
                flag = widget.feature.get_method(name)(event)
                if widget.capture_events is None:
                    if flag:
                        event.x = 9999
                elif widget.capture_events:
                    event.x = 9999
        self.trigger_config.update(cursor="arrow")

    def on_click(self, event: tkinter.Event, name: str) -> None:
        """Events to active the mouse"""
        self.focus_set()
        self.trigger_focus.reset()
        for widget in self.widgets[::-1]:
            if hasattr(widget, "feature") and not widget.disappeared:
                if widget.feature.get_method(name)(event) and widget.capture_events:
                    event.x = 9999
        self.trigger_focus.update(True, "")

    def on_release(self, event: tkinter.Event, name: str) -> None:
        """Events to release the mouse"""
        for widget in self.widgets[::-1]:
            if hasattr(widget, "feature") and not widget.disappeared:
                if widget.feature.get_method(name)(event) and widget.capture_events:
                    event.x = 9999

    def on_wheel(self, event: tkinter.Event, type_: bool | None) -> None:
        """Events to scroll the mouse wheel"""
        if type_ is not None:
            event.delta = 120 if type_ else -120
        for widget in self.widgets[::-1]:
            if hasattr(widget, "feature") and not widget.disappeared:
                if widget.feature.get_method("<MouseWheel>")(event) and widget.capture_events:
                    event.x = 9999

    def on_key_press(self, event: tkinter.Event) -> None:
        """Events for typing"""
        for widget in self.widgets[::-1]:
            if hasattr(widget, "feature") and not widget.disappeared:
                if widget.feature.get_method("<KeyPress>")(event) and widget.capture_events:
                    event.x = 9999

    def on_key_release(self, event: tkinter.Event) -> None:
        """Events for typing"""
        for widget in self.widgets[::-1]:
            if hasattr(widget, "feature") and not widget.disappeared:
                if widget.feature.get_method("<KeyRelease>")(event) and widget.capture_events:
                    event.x = 9999

    def register_event(
        self,
        name: str,
        *,
        add: bool | typing.Literal["", "+"] | None = None,
    ) -> str:
        """Register a event to process.

        * `name`: event name, such as "<Alt-A>"
        * `add`: whether it is an attached call

        In general, you don't need to call this method, but when the event to
        be bound is not in the predefined event, you need to manually call the
        method once.
        """
        def handle_event(event: tkinter.Event) -> None:
            for widget in self.widgets[::-1]:
                if hasattr(widget, "feature"):
                    if widget.feature.get_method(name)(event) and widget.capture_events:
                        pass

        return self.bind(name, handle_event, add)
