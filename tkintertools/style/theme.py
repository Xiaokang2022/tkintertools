"""Support for theme"""

import ctypes
import platform
import threading
import tkinter
import typing

import darkdetect

from ..color import rgb

DARK_MODE: bool = darkdetect.isDark()
THEME_MODE: typing.Literal["system", "dark", "light"] = "system"

_callback_events: dict[typing.Callable[[bool, typing.Any],
                                       typing.Any], tuple[typing.Any, ...]] = {}


def use_theme(__theme: typing.Literal["system", "dark", "light"], /) -> None:
    """
    Set the theme for the entire program

    theme can be light, dark, and follow the system, default is follow the system
    """
    global DARK_MODE, THEME_MODE
    THEME_MODE = __theme
    if __theme == "system":
        DARK_MODE = darkdetect.isDark()
    else:
        DARK_MODE = __theme == "dark"
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
    if THEME_MODE != "system":
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

    This class is only valid under Windows OS!
    """
    if platform.system() != "Windows":
        return
    tk.update()
    HWND = ctypes.windll.user32.GetParent(tk.winfo_id())
    if dark is None:
        dark = DARK_MODE
    if dark is not None:
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            HWND, 20, ctypes.byref(ctypes.c_int(dark)), 4)
    for i, value in enumerate((bordercolor, captioncolor, titlecolor)):
        if value is not None:
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                HWND, 34 + i, ctypes.byref(ctypes.c_int(rgb._str_to_hex(value, reverse=True))), 4)


threading.Thread(target=lambda: darkdetect.listener(
    _callback), daemon=True).start()
