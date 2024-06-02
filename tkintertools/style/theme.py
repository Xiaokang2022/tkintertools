"""Support for theme"""

import ctypes
import pathlib
import platform
import threading
import tkinter
import typing

import darkdetect

from ..color import rgb

__all__ = [
    "DARK_MODE",
    "COLOR_MODE",
    "SYSTEM_THEME_PATH",
    "selected_theme_path",
    "set_color_theme",
    "set_color_mode",
    "register_event",
    "remove_event",
    "custom_window",
]

DARK_MODE: bool = darkdetect.isDark()
COLOR_MODE: typing.Literal["system", "dark", "light"] = "system"
SYSTEM_THEME_PATH = pathlib.Path(__file__).parent.parent / "theme"

selected_theme_path = SYSTEM_THEME_PATH

_callback_events: dict[typing.Callable[[bool, typing.Any],
                                       typing.Any], tuple[typing.Any, ...]] = {}


def set_color_theme(theme_path: pathlib.Path | str = SYSTEM_THEME_PATH) -> bool:
    """
    Set a special color theme for the entire program

    color theme is a path of theme folder, default value is `system_theme_path`
    """
    global selected_theme_path
    selected_theme_path = pathlib.Path(theme_path)
    set_color_mode(COLOR_MODE)


def set_color_mode(color_mode: typing.Literal["system", "dark", "light"], /) -> None:
    """
    Set the color mode for the entire program

    color mode can be light, dark, and follow the system, default is follow the system
    """
    global DARK_MODE, COLOR_MODE
    COLOR_MODE = color_mode
    if color_mode == "system":
        DARK_MODE = darkdetect.isDark()
    else:
        DARK_MODE = color_mode == "dark"
    _process_event(DARK_MODE)


def register_event(
    func: typing.Callable[[bool, typing.Any], typing.Any],
    *args: typing.Any
) -> None:
    """
    When the system accent color changes, the registered function will be called,
    and the parameter is a boolean value indicating whether it is currently a dark theme

    * `func`: callback function
    * `args`: extra arguments
    """
    _callback_events[func] = args


def remove_event(func: typing.Callable[[bool, typing.Any], typing.Any]) -> None:
    """Remove a registered function"""
    del _callback_events[func]


def _process_event(dark: bool) -> None:
    """Handle registered callback functions"""
    for func, args in _callback_events.items():
        try:  # Prevent detection thread from crashing
            func(dark, *args)
        except:
            pass


def _callback(theme: str) -> None:
    """callback function that is triggered when a system theme is switched.
    Valid only if the theme mode is set to Follow System"""
    if COLOR_MODE != "system":
        return
    global DARK_MODE
    DARK_MODE = theme == "Dark"
    _process_event(DARK_MODE)


def custom_window(
    tk: tkinter.Tk,
    *,
    dark: bool | None = None,
    bordercolor: str | None = None,
    captioncolor: str | None = None,
    titlecolor: str | None = None,
) -> None:
    """
    Customize the relevant properties of the window

    * `tk`: root window
    * `dark`: dark mode
    * `bordercolor`: window border color
    * `captioncolor`: window caption color
    * `titlecolor`: window title color

    WARNING:

    This function is only works on Windows OS!
    """
    if platform.system() != "Windows":
        return
    tk.update()
    HWND = ctypes.windll.user32.GetParent(tk.winfo_id())
    if dark is None:
        dark = DARK_MODE
    if dark is not None:
        if ctypes.windll.dwmapi.DwmSetWindowAttribute(
                HWND, 20, ctypes.byref(ctypes.c_int(dark)), 4) != 0:
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                HWND, 19, ctypes.byref(ctypes.c_int(dark)), 4)
    for i, value in enumerate((bordercolor, captioncolor, titlecolor)):
        if value is not None:
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                HWND, 34 + i, ctypes.byref(ctypes.c_int(rgb._str_to_hex(value, reverse=True))), 4)


threading.Thread(target=lambda: darkdetect.listener(
    _callback), daemon=True).start()
