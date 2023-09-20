"""
core of tkintertools

Class Structure:

```text
+-------+         +-------------+
| tk.Tk |         | tk.Toplevel |
+-------+         +-------------+
    |                    |
    v                    v
+--------+        +--------------+        +--------------+
| tkt.Tk | -----> | tkt.Toplevel | -----> | tkt.NestedTk |
+--------+        +--------------+        +--------------+
                         |
                         v
                +-----------------+        +-------------+
                | tkt.BaseToolTip | -----> | tkt.ToolTip |
                +-----------------+        +-------------+

+-----------+        +------------+
| tk.Canvas | -----> | tkt.Canvas |
+-----------+        +------------+

+----------------+        +---------+
| tkt.BaseWidget | -----> | Widgets |
+----------------+        +---------+
```
"""

import ctypes
import platform
import tkinter
import typing

from .constants import *
from .exceptions import *

if platform.system() == 'Windows':
    if platform.win32_ver() == '6.1':  # Windows 7
        ctypes.windll.user32.SetProcessDPIAware()
    else:
        ctypes.WinDLL('shcore').SetProcessDpiAwareness(1)


class Tk(tkinter.Tk):
    """Root window"""

    def __init__(
        self,
        size: tuple[int, int] = SIZE,
        position: tuple[int, int] | tuple[None, None] | None = POSITION,
        *,
        title: str = TITLE,
        iconbitmap: str | None = ICONBITMAP,
        alpha: float = ALPHA,
        fullscreen: bool = FULLSCREEN,
        toolwindow: bool = TOOLWINDOW,
        topmost: bool = TOPMOST,
        transparentcolor: str | None = TRANSPARENTCOLOR,
        maxsize: tuple[int, int] = MAXSIZE,
        minsize: tuple[int, int] = MINSIZE,
        resizable: tuple[bool, bool] = RESIZABLE,
        overrideredirect: bool = OVERRIDEREDIRECT,
        shutdown: typing.Callable | None = SHUTDOWN,
        **kw
    ) -> None:
        """
        #### Positional Arguments
        * `size`: size of window, default is 200x200(px)
        * `position`: position of window, 'None' indicates a random location,
        default indicates that position is centered
        ---------------------------
        #### Keyword-only Arguments
        * `title`: title of window
        * `iconbitmap`: path to the window icon file
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
        #### Variable-length Keyword Arguments
        * `**kw`: compatible with other parameters of class tkinter.Tk, see tkinter.Tk for details
        """
        if self.__class__ == Tk:
            tkinter.Tk.__init__(self, **kw)

        self.title(title)
        if iconbitmap != ICONBITMAP:
            self.iconbitmap(default=iconbitmap)
        if alpha != ALPHA:
            self.attributes('-alpha', alpha)
        if fullscreen != FULLSCREEN:
            self.attributes('-fullscreen', fullscreen)
        if toolwindow != TOOLWINDOW:
            self.attributes('-toolwindow', toolwindow)
        if topmost != TOPMOST:
            self.attributes('-topmost', topmost)
        if transparentcolor != TRANSPARENTCOLOR:
            self.attributes('-transparentcolor', transparentcolor)
        if maxsize != MAXSIZE:
            self.maxsize(*maxsize)
        if minsize != MINSIZE:
            self.minsize(*minsize)
        if resizable != RESIZABLE:
            self.resizable(*resizable)
        if overrideredirect != OVERRIDEREDIRECT:
            self.overrideredirect(overrideredirect)
        if shutdown != SHUTDOWN:
            self.protocol('WM_DELETE_WINDOW', shutdown)

        self.ratio = [1., 1.]
        self.w, self.h = size
        self._init_w, self._init_h = size
        self._canvases: list[Canvas] = []

        if position == (None, None):  # random
            self.geometry(f'{self._init_w}x{self._init_h}')
        else:
            if position == POSITION:  # center
                x = (self.winfo_screenwidth() - self._init_w + DX) // 2
                y = (self.winfo_screenheight() - self._init_h) // 2
            else:
                x, y = position
            self.geometry(f'{self._init_w}x{self._init_h}+{x-DX}+{y}')

        self.bind('<Configure>', self._scale)

    def _scale(self, event: tkinter.Event, last_size: list[int] = [None]*2) -> None:
        """"""
        if (size := [event.width, event.height]) != last_size:
            self.ratio = [size[0]/self._init_w, size[1]/self._init_h]
            last_size[:] = size

    def child_canvas(self) -> tuple['Canvas']:
        """Returns all child canvas instances"""
        return tuple(filter(lambda x: hasattr(x, 'keep_ratio'), self.children.values()))


class Toplevel(tkinter.Toplevel, Tk):
    """Toplevel window"""

    def __init__(
        self,
        master: Tk | None = None,
        size: tuple[int, int] = SIZE,
        position: tuple[int, int] | tuple[None, None] | None = POSITION,
        *,
        title: str = TITLE,
        iconbitmap: str | None = ICONBITMAP,
        alpha: float = ALPHA,
        fullscreen: bool = FULLSCREEN,
        toolwindow: bool = TOOLWINDOW,
        topmost: bool = TOPMOST,
        transparentcolor: str | None = TRANSPARENTCOLOR,
        maxsize: tuple[int, int] = MAXSIZE,
        minsize: tuple[int, int] = MINSIZE,
        resizable: tuple[bool, bool] = RESIZABLE,
        overrideredirect: bool = OVERRIDEREDIRECT,
        shutdown: typing.Callable | None = SHUTDOWN,
        **kw
    ) -> None:
        """
        #### Positional Arguments
        * `master`: parent widget
        * `size`: size of window, default is 200x200(px)
        * `position`: position of window, 'None' indicates a random location,
        default indicates that position is centered
        ---------------------------
        #### Keyword-only Arguments
        * `title`: title of window, default is the same as title of master
        * `iconbitmap`: path to the window icon file
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
        #### Variable-length Keyword Arguments
        * `**kw`: compatible with other parameters of class tkinter.Toplevel, see tkinter.Toplevel for details
        """
        tkinter.Toplevel.__init__(self, master, **kw)
        if title == TITLE and master is not None:  # XXX
            title = master.title()
        Tk.__init__(self, size, position, title=title, iconbitmap=iconbitmap, alpha=alpha, fullscreen=fullscreen,
                    toolwindow=toolwindow, topmost=topmost, transparentcolor=transparentcolor, maxsize=maxsize,
                    minsize=minsize, resizable=resizable, overrideredirect=overrideredirect, shutdown=shutdown, **kw)
        self.focus_set()


class NestedTk(Toplevel):
    """"""

    def __init__(
        self,
        master: tkinter.Misc | tkinter.Wm,
        size: tuple[int, int] = SIZE,
        position: tuple[int, int] | tuple[None, None] | None = POSITION,
        *,
        title: str = TITLE,
        iconbitmap: str | None = ICONBITMAP,
        toolwindow: bool = TOOLWINDOW,
        transparentcolor: str | None = TRANSPARENTCOLOR,
        maxsize: tuple[int, int] = MAXSIZE,
        minsize: tuple[int, int] = MINSIZE,
        resizable: tuple[bool, bool] = RESIZABLE,
        overrideredirect: bool = OVERRIDEREDIRECT,
        shutdown: typing.Callable | None = SHUTDOWN,
        **kw
    ) -> None:
        """"""
        if (system := platform.system()) != 'Windows':
            raise SystemError(system)
        Toplevel.__init__(self, master, size, position, title=title, iconbitmap=iconbitmap, toolwindow=toolwindow,
                          transparentcolor=transparentcolor, maxsize=maxsize, minsize=minsize,
                          resizable=resizable, overrideredirect=overrideredirect, shutdown=shutdown, **kw)
        self.master = master
        self.after(1, self._nested)

    def _nested(self) -> None:
        """"""
        handle = ctypes.WinDLL('user32').GetParent(self.winfo_id())
        ctypes.WinDLL('user32').SetParent(handle, self.master.winfo_id())
        self.master.focus_set()


class Canvas(tkinter.Canvas):
    """"""

    def __init__(
        self,
        master=None,  # type: Tk | 'Canvas' | None
        *,
        keep_ratio: bool = False,  # only for 'place' manager
        auto_scale: bool = False,  # only for 'place' manager
        **kw,
    ) -> None:
        """
        #### Positional Arguments
        * `master`: 
        #### Keyword-only Arguments
        * `keep_ratio`: 
        * `auto_scale`: 
        #### Variable-length Keyword Arguments
        * `**kw`: 
        """
        tkinter.Canvas.__init__(self, master, **kw)
        self.master: Tk | Canvas = master
        self.keep_ratio = keep_ratio
        self.auto_scale = auto_scale
        self._init_ratio: float = None
        self._init_width: int = None
        self._init_height: int = None
        self.live = True  # XXX

        self._canvases: list[Canvas] = []
        self._widgets: list[BaseWidget] = []
        self._items: list[int] = []

        self.master._canvases.append(self)

        self.bind('<Motion>', self._touch)
        self.bind('<Any-Key>', self._input)
        self.bind('<Button-1>', self._click)
        self.bind('<B1-Motion>', self._click)
        self.bind('<MouseWheel>', self._mousewheel)
        self.bind('<ButtonRelease-1>', self._release)
        self.bind('<<Copy>>', self._copy)
        self.bind('<<Paste>>', self._paste)
        self.bind('<Configure>', self._scale)

    def _scale(self, event: tkinter.Event) -> None:
        """scale content"""  # TODO
        if self._init_width is None:
            self._init_width = event.width
            self._init_height = event.height
            self._init_ratio = event.width / event.height
            return
        ratio_x = event.width / self._init_width
        ratio_y = event.height / self._init_height
        for widget in self._widgets:
            widget.scale_absolute(ratio_x, ratio_y)  # modify data XXX

        # modify screen BUG
        for item in self.find_withtag('x'):
            self.coords(
                item, *[c*(ratio_x, 1)[i & 1] for i, c in enumerate(self.coords(item))])
        for item in self.find_withtag('y'):
            self.coords(
                item, *[c*(1, ratio_y)[i & 1] for i, c in enumerate(self.coords(item))])
        for item in self.find_withtag('xy'):
            self.coords(
                item, *[c*(ratio_x, ratio_y)[i & 1] for i, c in enumerate(self.coords(item))])

        if self.auto_scale is False or self.winfo_manager() != 'place':
            return
        if self.keep_ratio is True:
            pass
        """scale self"""

    def _touch(self, event: tkinter.Event) -> None:
        """"""
        for widget in self._widgets[::-1]:
            if widget.state_hover(event):
                return
        else:
            self.configure(cursor='arrow')

    def _click(self, event: tkinter.Event, _flag: bool = False) -> None:
        """"""
        for widget in self._widgets[::-1]:
            if _flag:
                widget.state(State.DEFAULT)
            elif widget.state_selected(event):
                _flag = True

    def _release(self, event: tkinter.Event) -> None:
        """"""
        for widget in self._widgets[::-1]:
            if widget.state_hover(event):
                return

    def _mousewheel(self, event: tkinter.Event) -> None:
        """"""
        for widget in self._widgets[::-1]:
            if widget.scroll(event):
                return

    def _input(self, event: tkinter.Event) -> None:
        """"""
        for widget in self._widgets[::-1]:
            if widget.input(event):
                return

    def _copy(self, event: tkinter.Event) -> None:
        """"""
        for widget in self._widgets[::-1]:
            if widget.copy(event):
                return

    def _paste(self, event: tkinter.Event) -> None:
        """"""
        for widget in self._widgets[::-1]:
            if widget.paste(event):
                return

    def _keep(self) -> None:
        """"""
        self.winfo_width()


class BaseToolTip(Toplevel):
    """"""

    def __init__(
        self,
        master: Tk | None = None,
        position: tuple[int, int] | tuple[None, None] | None = POSITION,
        *,
        transparentcolor: str | None = TRANSPARENTCOLOR,
        duration: int = float('inf'),
        animation: bool = False,
        **kw
    ) -> None:
        """"""
        Toplevel.__init__(self, master, SIZE, position, transparentcolor=transparentcolor,
                          resizable=(False, False), overrideredirect=True, **kw)
        self.withdraw()
        self.duration = duration
        self.animation = animation

    def show(self, x: int, y: int) -> None:
        """"""
        self.deiconify()

    def _animate(self) -> None:
        """"""

    def _countdown(self) -> None:
        """"""

    def _cancel(self) -> None:
        """"""

    def _destroy(self) -> None:
        """"""


class ToolTip(BaseToolTip):
    """"""

    def __init__(
        self,
        master: Tk | None = None,
        position: tuple[int, int] | tuple[None, None] | None = POSITION,
        *,
        transparentcolor: str | None = TRANSPARENTCOLOR,
        duration: int = float('inf'),
        animation: bool = False,
        **kw
    ) -> None:
        """"""


class BaseWidget:
    """The base class for the widget class"""

    def __init__(
        self,
        canvas: Canvas,
        x: int,
        y: int,
        width: int,
        height: int,
        /,
        *,
        resize: bool = False,
        minsize: tuple[int, int] = (0,) * 2,
        maxsize: tuple[int, int] = (float('inf'),) * 2,
        expand: typing.Literal['', 'x', 'y', 'xy'] = Expand.XY,
        state: typing.Literal['default', 'hover', 'selected',
                              'disabled', 'error'] = State.DEFAULT,
    ) -> None:
        """"""
        self.canvas = canvas
        self.resize = resize
        self.expand = expand
        self.minsize = minsize
        self.maxsize = maxsize
        self._state = state
        self.x = self._init_x = x
        self.y = self._init_y = y
        self.width = self._init_width = width
        self.height = self._init_height = height
        self._items: dict[str, int] = {}
        self.canvas._widgets.append(self)

    def state(self, state_: typing.Literal['default', 'hover', 'selected', 'disabled', 'error'] | None = None, /) -> State | None:
        """"""
        if state_ is None:
            return self._state
        if state_ not in State._value2member_map_:
            raise StateError(state_)
        self._state = state_
        eval(f'self.state_{state_}()')  # FIXME

    def destroy(self) -> None:
        """"""
        self.canvas.delete(*self._items.values())
        self._items.clear()

    def move(self, dx: int, dy: int) -> None:
        """"""
        self.x += dx
        self.y += dy
        for item in self._items.values():
            self.canvas.move(item, dx, dy)

    def move_to(self, x: int, y: int) -> None:
        """"""
        self.move(x - self.x, y - self.y)

    def scale_absolute(self, ratio_x: float, ratio_y: float) -> None:
        """"""
        if 'x' in self.expand:
            self.x = self._init_x * ratio_x
        if 'y' in self.expand:
            self.y = self._init_y * ratio_y
        if self.resize is True:
            self.width = self._init_width * ratio_x
            self.height = self._init_height * ratio_y
        self.scale_callback(ratio_x, ratio_y, 'absolute')

    def scale_relative(self, ratio_x: float, ratio_y: float) -> None:
        """"""
        if 'x' in self.expand:
            self.x *= ratio_x
        if 'y' in self.expand:
            self.y *= ratio_y
        if self.resize is True:
            self.width *= ratio_x
            self.height *= ratio_y
        self.scale_callback(ratio_x, ratio_y, 'relative')

    def scale_callback(self, ratio_x: float, ratio_y: float, type_: typing.Literal['absolute', 'relative']) -> None:
        """"""

    def state_default(self, event: tkinter.Event) -> bool:
        """"""
        return False

    def state_hover(self, event: tkinter.Event) -> bool:
        """"""
        return False

    def state_selected(self, event: tkinter.Event) -> bool:
        """"""
        return False

    def state_disabled(self, event: tkinter.Event) -> bool:
        """"""
        return False

    def state_error(self, event: tkinter.Event) -> bool:
        """"""
        return False

    def scroll(self, event: tkinter.Event) -> bool:
        """"""
        return False

    def input(self, event: tkinter.Event) -> bool:
        """"""
        return False

    def copy(self, event: tkinter.Event) -> bool:
        """"""
        return False

    def paste(self, event: tkinter.Event) -> bool:
        """"""
        return False
