"""Some useful utility classes or utility functions"""

import ctypes
import platform
import typing

__all__ = [
    "load_font",
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


def load_font(font_path: str | bytes, *, private: bool = True, enumerable: bool = False) -> bool:
    """
    Makes fonts located in file `font_path` available to the font system

    * `font_path`: the font file path
    * `private`: if True, other processes cannot see this font,
    and this font will be unloaded when the process dies
    * `enumerable`: if True, this font will appear when enumerating fonts

    TIP:

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
