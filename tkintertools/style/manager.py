"""Support for theme

* darkdetect: https://github.com/albertosottile/darkdetect
* pywinstyles: https://github.com/Akascape/py-window-styles
* win32material: https://github.com/littlewhitecloud/win32material
* hPyT: https://github.com/Zingzy/hPyT
"""

from __future__ import annotations

__all__ = [
    "set_color_mode",
    "get_color_mode",
    "set_theme_map",
    "register_event",
    "remove_event",
    "customize_window",
]

import collections.abc
import ctypes.wintypes
import platform
import threading
import tkinter
import traceback
import types
import typing

from ..core import configs
from ..toolbox import tools
from . import parser

try:
    import darkdetect
except ImportError:
    pass

try:
    import pywinstyles
except ImportError:
    pass

try:
    import hPyT
except ImportError:
    pass

try:
    import win32material
except ImportError:
    pass

_callback_events: dict[collections.abc.Callable[[bool, typing.Any], typing.Any], tuple] = {}
"""Events that are responded to when the system theme changes"""


def set_color_mode(mode: typing.Literal["system", "dark", "light"] = "system") -> None:
    """Set the color mode of the program

    * `mode`: it can be `"light"`, `"dark"`, and `"system"`

    TIP:

    `"system"` is the following system
    """
    configs.Theme.color_mode = mode
    _process_event(configs.Env.is_dark if mode == "system" else (mode == "dark"))


def get_color_mode() -> typing.Literal["dark", "light"]:
    """Get the color mode of the program"""
    if configs.Theme.color_mode == "system":
        return "dark" if configs.Env.is_dark else "light"
    return configs.Theme.color_mode


def set_theme_map(
    *,
    light_theme: str | types.ModuleType | None = None,
    dark_theme: str | types.ModuleType | None = None,
) -> None:
    """Set the path to the theme file used by the current program

    * `light_theme`: the name of the theme of the light theme
    * `dark_theme`: the name of the theme of the dark theme
    """
    if dark_theme is not None:
        configs.Theme.dark = dark_theme
    if light_theme is not None:
        configs.Theme.light = light_theme
    if any((light_theme, dark_theme)):
        parser.get_file.cache_clear()


def register_event(
    func: collections.abc.Callable[[bool, typing.Any], typing.Any],
    *args: typing.Any,
) -> None:
    """When the system accent color changes, the registered function will be called, and the
    parameter is a boolean value indicating whether it is currently a dark theme

    * `func`: callback function
    * `args`: extra arguments
    """
    _callback_events[func] = args


def remove_event(func: collections.abc.Callable[[bool, typing.Any], typing.Any]) -> None:
    """Remove a registered function

    * `func`: callback function
    """
    if _callback_events.get(func) is not None:
        del _callback_events[func]


def customize_window(
    window: tkinter.Tk,
    *,
    style: typing.Literal["mica", "acrylic", "aero", "transparent", "optimised",
                          "win7", "inverse", "native", "popup", "dark", "normal"] | None = None,
    border_color: str | None = None,
    header_color: str | None = None,
    title_color: str | None = None,
    enable_file_dnd: collections.abc.Callable[[str], typing.Any] | None = None,
    hide_title_bar: bool | None = None,
    hide_button: typing.Literal["all", "maxmin", "none"] | None = None,
    disable_minimize_button: bool | None = None,
    disable_maximize_button: bool | None = None,
    boarder_type: typing.Literal["rectangular", "smallround", "round"] | None = None,
) -> None:
    """Customize the relevant properties of the window

    * `window`: the window which being customized
    * `style`: different styles for windows
    * `border_color`: border color of the window
    * `header_color`: header color of the window
    * `title_color`: title color of the window
    * `enable_file_dnd`: apply file drag and drop in window
    * `hide_title_bar`: Wether hide the whole title bar
    * `hide_button`: Wether hide part of buttons on title bar
    * `disable_minimize_button`: Wether disable minimize button
    * `disable_maximize_button`: Wether disable maximize button
    * `boarder_type`: boarder type of the window

    WARNING:

    This function is only works on Windows OS! And some parameters are useless on Windows 7/10!
    """
    if globals().get("pywinstyles") is not None:
        if style is not None:
            pywinstyles.apply_style(window, style)
            # This is a flaw in `pywinstyles`, which is fixed here
            if platform.win32_ver()[0] == "10":
                window.withdraw()
                window.deiconify()
                window.update()
        if border_color is not None:
            pywinstyles.change_border_color(window, border_color)
        if header_color is not None:
            pywinstyles.change_header_color(window, header_color)
        if title_color is not None:
            pywinstyles.change_title_color(window, title_color)
        if enable_file_dnd is not None:
            pywinstyles.apply_dnd(tools.get_hwnd(window), enable_file_dnd)

    if globals().get("hPyT") is not None:
        if hide_title_bar is not None:
            if hide_title_bar:
                hPyT.title_bar.hide(window)
            else:
                hPyT.title_bar.unhide(window)
        if hide_button is not None:
            if hide_button == "maxmin":
                hPyT.maximize_minimize_button.hide(window)
            elif hide_button == "all":
                hPyT.all_stuffs.hide(window)
            else:
                hPyT.maximize_minimize_button.unhide(window)
                hPyT.all_stuffs.unhide(window)
        if disable_maximize_button is not None:
            if disable_maximize_button:
                hPyT.maximize_button.disable(window)
            else:
                hPyT.maximize_button.enable(window)
        if disable_minimize_button is not None:
            if disable_minimize_button:
                hPyT.minimize_button.disable(window)
            else:
                hPyT.minimize_button.enable(window)

    if globals().get("win32material") is not None:
        if boarder_type is not None:
            match boarder_type:
                case "rectangular": type_ = win32material.BORDERTYPE.RECTANGULAR
                case "smallround": type_ = win32material.BORDERTYPE.SMALLROUND
                case "round": type_ = win32material.BORDERTYPE.ROUND
            win32material.SetWindowBorder(ctypes.wintypes.HWND(tools.get_hwnd(window)), type_)


def _process_event(dark_mode: bool) -> None:
    """Handle registered callback functions

    * `dark_mode`: Wether it is dark mode
    """
    for func, args in _callback_events.items():
        try:  # Prevent detection thread from crashing
            func(dark_mode, *args)
        except Exception as exc:
            traceback.print_exception(exc)


def _callback(theme: str) -> None:
    """Callback function that is triggered when a system theme is switched. Valid only if the theme
    mode is set to Follow System

    * `theme`: theme name
    """
    configs.Env.is_dark = theme == "Dark"
    if configs.Theme.color_mode == "system":
        _process_event(configs.Env.is_dark)


if globals().get("darkdetect") is not None:
    threading.Thread(target=lambda: darkdetect.listener(_callback), daemon=True).start()
