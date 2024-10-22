"""Some useful utility classes or utility functions"""

# pylint: disable=protected-access

__all__ = [
    "get_hwnd",
    "embed_window",
    "load_font",
    "screen_size",
    "get_text_size",
]

import atexit
import ctypes
import os
import platform
import shutil
import tkinter
import tkinter.font
import traceback
import typing

from ..core import constants, virtual


_LINUX_FONTS_DIR = os.path.expanduser("~/.fonts/")


class _Trigger:
    """Single trigger

    It can only be triggered once before the reset, and multiple triggers are
    invalid. When triggered, the callback function is called.
    """

    def __init__(self, command: typing.Callable) -> None:
        """
        * `command`: the function that is called when triggered
        """
        self._flag: bool = False
        self._lock: bool = False
        self._command = command

    def get(self) -> bool:
        """Get the status of the trigger"""
        return self._flag

    def reset(self) -> None:
        """Reset the status of the trigger"""
        if not self._lock:
            self._flag = False

    def lock(self) -> None:
        """Lock the trigger so that it can't be updated"""
        self._lock = True

    def unlock(self) -> None:
        """Unlock this trigger so that it can be updated again"""
        self._lock = False

    def update(self, value: bool = True, /, *args, **kwargs) -> None:
        """Update the status of the trigger

        `value`: updated value
        """
        if not self._lock and not self._flag and value:
            self._flag = True
            self._command(*args, **kwargs)


def get_hwnd(widget: tkinter.Widget) -> int:
    """Get the HWND of `tkinter.Widget`"""
    return ctypes.windll.user32.GetParent(widget.winfo_id())


def embed_window(
    window: tkinter.Misc,
    parent: tkinter.Misc | None,
    *,
    focus: bool = False,
) -> None:
    """Embed a widget into another widget

    * `window`: Widget that will be embedded in
    * `parent`: parent widget, `None` indicates that the parent widget is the
    screen
    * `focus`: whether direct input focus to this window
    """
    ctypes.windll.user32.SetParent(
        get_hwnd(window), parent.winfo_id() if parent else None)

    if not focus:
        window.master.focus_set()


def load_font(
    font_path: str | bytes,
    *,
    private: bool = True,
    enumerable: bool = False,
) -> bool:
    """Make fonts located in file `font_path` available to the font system, and
    return `True` if the operation succeeds, `False` otherwise

    * `font_path`: the font file path
    * `private`: if True, other processes cannot see this font(Only Windows OS),
    and this font will be unloaded when the process dies
    * `enumerable`: if True, this font will appear when enumerating fonts(Only
    Windows OS)

    ATTENTION:

    * This function is referenced from `customtkinter.FontManager.load_font`,
    CustomTkinter: https://github.com/TomSchimansky/CustomTkinter
    * This function only works on Windows and Linux OS
    """
    if platform.system() == "Windows":
        if isinstance(font_path, str):
            path_buffer = ctypes.create_unicode_buffer(font_path)
            add_font_resource_ex = ctypes.windll.gdi32.AddFontResourceExW
        elif isinstance(font_path, bytes):
            path_buffer = ctypes.create_string_buffer(font_path)
            add_font_resource_ex = ctypes.windll.gdi32.AddFontResourceExA
        else:
            raise TypeError("`font_path` must be of type `str` or `byte`.")

        flags = (0x10 if private else 0) | (0x20 if not enumerable else 0)
        num_fonts_added = add_font_resource_ex(
            ctypes.byref(path_buffer), flags, 0)

        return bool(min(num_fonts_added, 1))

    elif platform.system() == "Linux":
        try:
            os.makedirs(_LINUX_FONTS_DIR, exist_ok=True)
            shutil.copy(font_path, _LINUX_FONTS_DIR)

            if private:
                atexit.register(
                    os.remove, _LINUX_FONTS_DIR + font_path.rsplit("/", 1)[-1])

            return True
        except Exception as exc:
            traceback.print_exception(exc)
            return False

    return False


def screen_size() -> tuple[int, int]:
    """Return the size of the screen"""
    if tkinter._default_root is None:
        temp_tk = tkinter.Tk()
        temp_tk.withdraw()
        width = temp_tk.winfo_screenwidth()
        height = temp_tk.winfo_screenheight()
        temp_tk.destroy()
        return width, height

    width = tkinter._default_root.winfo_screenwidth()
    height = tkinter._default_root.winfo_screenheight()
    return width, height


if platform.system() == "Windows":

    __all__.append("set_mouse_position")

    def set_mouse_position(x: int, y: int) -> None:
        """Set mouse cursor position

        ATTENTION:

        This function only works on Windows OS!
        """
        ctypes.windll.user32.SetCursorPos(x, y)


def get_text_size(
    text: str,
    fontsize: int | None = None,
    family: str | None = None,
    *,
    padding: int = 0,
    master: tkinter.Canvas | virtual.Widget | None = None,
    **kwargs,
) -> tuple[int, int]:
    """Get the size of a text with a special font family and font size

    * `text`: the text
    * `fontsize`: font size of the text
    * `family`: font family of the text
    * `padding`: extra padding of the size
    * `master`: default canvas or widget provided
    * `kwargs`: kwargs of `tkinter.font.Font`

    ATTENTION:

    * This function only works when the fontsize is negative number!
    """
    if family is None:
        family = constants.FONT
    if fontsize is None:
        fontsize = constants.SIZE

    fontsize = -abs(fontsize)
    temp_cv = master if master else tkinter.Canvas(tkinter._default_root)
    while isinstance(temp_cv, virtual.Widget):
        temp_cv = temp_cv.master
    font = tkinter.font.Font(family=family, size=fontsize, **kwargs)
    item = temp_cv.create_text(-9999, -9999, text=text, font=font)
    x1, y1, x2, y2 = temp_cv.bbox(item)
    temp_cv.delete(item)
    if master is None:
        temp_cv.destroy()
    return 2*padding + x2 - x1, 2*padding + y2 - y1
