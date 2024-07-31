"""Some useful utility classes or utility functions"""

import ctypes
import inspect
import platform
import tkinter
import tkinter.font
import typing

from ..core import constants

__all__ = [
    "get_hwnd",
    "embed_window",
    "load_font",
    "screen_size",
    "set_mouse_position",
    "get_text_size",
]


class _Trigger:
    """Single trigger"""

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

    def update(self, value: bool = True, *args, **kwargs) -> None:
        """
        Update the status of the trigger

        `value`: updated value
        """
        if not self._lock and not self._flag and value:
            self._flag = True
            self._command(*args, **kwargs)


def get_hwnd(widget: tkinter.Widget) -> int:
    """Get the HWND of a widget"""
    return ctypes.windll.user32.GetParent(widget.winfo_id())


def embed_window(
    window: tkinter.Misc,
    parent: tkinter.Misc | None,
    *,
    focus: bool = False,
) -> None:
    """
    Embed a widget into another widget

    * `window`: Widget that will be embedded in
    * `parent`: parent widget, None indicates the screen
    * `focus`: whether direct input focus to this window
    """
    ctypes.windll.user32.SetParent(
        get_hwnd(window), parent.winfo_id() if parent else None)
    if not focus:
        window.master.focus_set()


def load_font(font_path: str | bytes, *, private: bool = True, enumerable: bool = False) -> bool:
    """
    Makes fonts located in file `font_path` available to the font system

    * `font_path`: the font file path
    * `private`: if True, other processes cannot see this font,
    and this font will be unloaded when the process dies
    * `enumerable`: if True, this font will appear when enumerating fonts

    TIPS:

    This function is referenced from `customtkinter.FontManager.load_font`,
    CustomTkinter: https://github.com/TomSchimansky/CustomTkinter
    """
    if platform.system() == "Windows":
        if isinstance(font_path, str):
            path_buffer = ctypes.create_unicode_buffer(font_path)
            add_font_resource_ex = ctypes.windll.gdi32.AddFontResourceExW
        elif isinstance(font_path, bytes):
            path_buffer = ctypes.create_string_buffer(font_path)
            add_font_resource_ex = ctypes.windll.gdi32.AddFontResourceExA

        flags = (0x10 if private else 0) | (0x20 if not enumerable else 0)
        num_fonts_added = add_font_resource_ex(
            ctypes.byref(path_buffer), flags, 0)

        return bool(min(num_fonts_added, 1))

    elif platform.system() == "Linux":
        pass

    return False


def screen_size() -> tuple[int, int]:
    """Return the width and height of the screen"""
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


def set_mouse_position(x: int, y: int) -> None:
    """
    Set mouse cursor position

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
) -> tuple[int, int]:
    """
    Get the size of a text with a special font family and font size

    * `text`: the text
    * `fontsize`: font size of the text
    * `family`: font family of the text
    * `padding`: extra padding of the size

    ATTENTION:

    This function only works when the fontsize is under zero!
    And when there is a line break, the return value will be inaccurate!
    """
    if family is None:
        family = constants.FONT
    if fontsize is None:
        fontsize = constants.SIZE
    if fontsize > 0:
        raise ValueError("The fontsize is required under zero.")
    width = tkinter.font.Font(family=family, size=fontsize).measure(text)
    return 2*padding + width, 2*padding - fontsize
