"""Some useful utility classes or utility functions."""

from __future__ import annotations

__all__ = [
    "get_parent",
    "embed_window",
    "load_font",
    "screen_size",
    "get_text_size",
    "fix_cursor",
    "create_smoke",
]

import atexit
import collections.abc
import ctypes
import os
import platform
import shutil
import tkinter
import tkinter.font
import traceback
import typing

from ..core import configs, virtual
from . import enhanced

try:
    from PIL import Image
except ImportError:
    Image = None


class Trigger:
    """Single trigger.

    It can only be triggered once before the reset, and multiple triggers are
    invalid. When triggered, the callback function is called.
    """

    def __init__(
        self,
        command: collections.abc.Callable[..., typing.Any],
    ) -> None:
        """
        * `command`: the function that is called when triggered
        """
        self._flag: bool = False
        self._lock: bool = False
        self._command = command

    def get(self) -> bool:
        """Get the status of the trigger."""
        return self._flag

    def reset(self) -> None:
        """Reset the status of the trigger."""
        if not self._lock:
            self._flag = False

    def lock(self) -> None:
        """Lock the trigger so that it can't be updated."""
        self._lock = True

    def unlock(self) -> None:
        """Unlock this trigger so that it can be updated again."""
        self._lock = False

    def update(self, value: bool = True, /, *args, **kwargs) -> None:
        """Update the status of the trigger.

        * `value`: updated value
        * `args`: args of the command
        * `kwargs`: kwargs of the command
        """
        if not self._lock and not self._flag and value:
            self._flag = True
            self._command(*args, **kwargs)


def get_parent(widget: tkinter.Misc) -> int:
    """Get the HWND of `tkinter.Widget`.

    * `widget`: the widget
    """
    return ctypes.windll.user32.GetParent(widget.winfo_id())


def embed_window(
    window: tkinter.Misc,
    parent: tkinter.Misc | None,
    *,
    focus: bool = False,
) -> None:
    """Embed a widget into another widget.

    * `window`: Widget that will be embedded in
    * `parent`: parent widget, `None` indicates that the parent widget is the screen
    * `focus`: whether direct input focus to this window
    """
    ctypes.windll.user32.SetParent(
        get_parent(window), parent.winfo_id() if parent else None)

    if not focus and window.master is not None:
        window.master.focus_set()


def load_font(
    font_path: str | bytes,
    *,
    private: bool = True,
    enumerable: bool = False,
) -> bool:
    """Make fonts located in file `font_path` available to the font system, and
    return `True` if the operation succeeds, `False` otherwise.

    * `font_path`: the font file path
    * `private`: if True, other processes cannot see this font(Only Windows OS),
    and this font will be unloaded when the process dies
    * `enumerable`: if True, this font will appear when enumerating fonts(Only Windows OS)

    This function only works on Windows and Linux OS.

    This function is referenced from `customtkinter.FontManager.load_font`,
    CustomTkinter: https://github.com/TomSchimansky/CustomTkinter.
    """
    if platform.system() == "Windows":
        if isinstance(font_path, str):
            path_buffer = ctypes.create_unicode_buffer(font_path)
            add_font_resource_ex = ctypes.windll.gdi32.AddFontResourceExW
        else:
            path_buffer = ctypes.create_string_buffer(font_path)
            add_font_resource_ex = ctypes.windll.gdi32.AddFontResourceExA

        flags = (0x10 if private else 0) | (0x20 if not enumerable else 0)
        num_fonts_added = add_font_resource_ex(
            ctypes.byref(path_buffer), flags, 0)

        return bool(min(num_fonts_added, 1))

    if platform.system() == "Linux":
        if isinstance(font_path, bytes):
            font_path = font_path.decode()

        linux_fonts_dir = os.path.expanduser("~/.fonts/")

        try:
            os.makedirs(linux_fonts_dir, exist_ok=True)
            shutil.copy(font_path, linux_fonts_dir)

            if private:
                atexit.register(
                    os.remove, linux_fonts_dir + font_path.rsplit("/", 1)[-1])

            return True
        except Exception as exc:  # pylint: disable=W0718
            traceback.print_exception(exc)

    return False


def screen_size() -> tuple[int, int]:
    """Returns the size of the screen."""
    width = configs.Env.root.winfo_screenwidth()
    height = configs.Env.root.winfo_screenheight()
    return width, height


def get_text_size(
    text: str,
    fontsize: int | None = None,
    family: str | None = None,
    *,
    padding: int = 0,
    master: tkinter.Canvas | virtual.Widget | None = None,
    **kwargs,
) -> tuple[int, int]:
    """Get the size of a text with a special font family and font size.

    * `text`: the text
    * `fontsize`: font size of the text
    * `family`: font family of the text
    * `padding`: extra padding of the size
    * `master`: default canvas or widget provided
    * `kwargs`: kwargs of `tkinter.font.Font`

    This function only works when the fontsize is negative number!
    """
    if family is None:
        family = configs.Font.family
    if fontsize is None:
        fontsize = configs.Font.size

    fontsize = -abs(fontsize)
    temp_cv = master if master else tkinter.Canvas(configs.Env.root)

    while isinstance(temp_cv, virtual.Widget):
        temp_cv = temp_cv.master

    font = tkinter.font.Font(temp_cv, family=family, size=fontsize, **kwargs)
    item = temp_cv.create_text(-9999, -9999, text=text, font=font)
    x1, y1, x2, y2 = temp_cv.bbox(item)
    temp_cv.delete(item)

    if master is None:
        temp_cv.destroy()

    return 2*padding + x2 - x1, 2*padding + y2 - y1


def fix_cursor(name: str, /) -> str:
    """Fix the cursor name.

    * `name`: name of cursor
    """
    if name == "disabled":
        match platform.system():
            case "Windows": return "no"
            case "Darwin": return "notallowed"
            case _: return "arrow"

    return name


def create_smoke(
    size: tuple[int, int],
    *,
    color: str | tuple[int, int, int, int] = "#00000066",
) -> enhanced.PhotoImage:
    """Create a temporary smoke zone. Return the `enhanced.PhotoImage`.

    * `size`: size of the smoke zone
    * `color`: color of the smoke zone

    This function need `PIL` to run.

    About the "smoke", see: https://fluent2.microsoft.design/material#smoke
    """
    if Image is None:
        raise RuntimeError("Package 'pillow' is missing.")

    # When you have 'PIL.Image', you definitely have 'PIL.ImageTk'
    return enhanced.PhotoImage(Image.new("RGBA", size, color))
