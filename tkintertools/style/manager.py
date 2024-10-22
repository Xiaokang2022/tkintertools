"""Support for theme

All third packages which relative to style introduced by `tkintertools` are
there:

* darkdetect: https://github.com/albertosottile/darkdetect
* pywinstyles: https://github.com/Akascape/py-window-styles
* win32material: https://github.com/littlewhitecloud/win32material
* hPyT: https://github.com/Zingzy/hPyT
"""

__all__ = [
    "SYSTEM_DARK_MODE",
    "set_color_mode",
    "get_color_mode",
    "set_theme_map",
    "get_theme_map",
    "reset_theme_map",
    "register_event",
    "remove_event",
    "customize_window",
]

import pathlib
import platform
import threading
import tkinter
import traceback
import types
import typing

from ..theme import dark, light
from ..toolbox import tools
from . import parser

try:
    import darkdetect
except ImportError:
    darkdetect = None

try:
    import pywinstyles
except ImportError:
    pywinstyles = None

try:
    import hPyT
except ImportError:
    hPyT = None

try:
    import win32material
except ImportError:
    win32material = None

SYSTEM_DARK_MODE: bool = bool(darkdetect.isDark()) if darkdetect else False

_theme_map: dict[typing.Literal["dark", "light"], pathlib.Path |
                 str | types.ModuleType] = {"dark": dark, "light": light}
"""
The mapping table between dark and light themes, when the program switches to a
light color, it will use the theme of the light color in the map, and the same
goes for dark colors
"""

_color_mode: typing.Literal["system", "light", "dark"] = "system"
"""
The color mode of the current program, `"system"` is the following system,
`"light"` is the light color, and `"dark"` is the dark color
"""

_callback_events: dict[typing.Callable[[bool, typing.Any], typing.Any],
                       tuple[typing.Any, ...]] = {}
"""Events that are responded to when the system theme changes"""


def set_color_mode(
    mode: typing.Literal["system", "dark", "light"] = "system",
) -> None:
    """Set the color mode of the program

    * `mode`: it can be `"light"`, `"dark"`, and `"system"`

    TIP:

    `"system"` is the following system
    """
    global _color_mode
    _color_mode = mode
    _process_event(SYSTEM_DARK_MODE if mode == "system" else (mode == "dark"))


def get_color_mode() -> typing.Literal["dark", "light"]:
    """Get the color mode of the program"""
    if _color_mode == "system":
        return "dark" if SYSTEM_DARK_MODE else "light"
    return _color_mode


def set_theme_map(
    *,
    light: str | types.ModuleType | None = None,
    dark: str | types.ModuleType | None = None,
) -> None:
    """Set the path to the theme file used by the current program

    * `light`: the name of the theme of the light theme
    * `dark`: the name of the theme of the dark theme
    """
    if dark is not None:
        _theme_map["dark"] = dark
    if light is not None:
        _theme_map["light"] = light
    if any((light, dark)):
        parser._get_file.cache_clear()


def get_theme_map() -> dict[typing.Literal["dark", "light"],
                            str | pathlib.Path | types.ModuleType]:
    """Get the theme map"""
    return _theme_map.copy()


def reset_theme_map() -> None:
    """Reset the value of theme map"""
    _theme_map.update(dark=dark, light=light)


def register_event(
    func: typing.Callable[[bool, typing.Any], typing.Any],
    *args: typing.Any,
) -> None:
    """When the system accent color changes, the registered function will be
    called, and the parameter is a boolean value indicating whether it is
    currently a dark theme

    * `func`: callback function
    * `args`: extra arguments
    """
    _callback_events[func] = args


def remove_event(func: typing.Callable[[bool, typing.Any], typing.Any]) -> None:
    """Remove a registered function

    * `func`: callback function
    """
    if _callback_events.get(func) is not None:
        del _callback_events[func]


def customize_window(
    window: tkinter.Tk,
    *,
    style: typing.Literal["mica", "acrylic", "aero", "transparent",
                          "optimised", "win7", "inverse", "native",
                          "popup", "dark", "normal"] | None = None,
    border_color: str | None = None,
    header_color: str | None = None,
    title_color: str | None = None,
    enable_file_dnd: typing.Callable[[str], typing.Any] | None = None,
    hide_title_bar: bool | None = None,
    hide_button: typing.Literal["all", "maxmin", "none"] | None = None,
    disable_minimize_button: bool | None = None,
    disable_maximize_button: bool | None = None,
    boarder_type: typing.Literal["rectangular",
                                 "smallround", "round"] | None = None,
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

    This function is only works on Windows OS!
    And some parameters are useless on Windows 7/10!
    """
    if pywinstyles:
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
            pywinstyles.apply_dnd(window, enable_file_dnd)

    if hPyT:
        if hide_title_bar is not None:
            hPyT.title_bar.hide(
                window) if hide_title_bar else hPyT.title_bar.unhide(window)
        if hide_button is not None:
            if hide_button == "maxmin":
                hPyT.maximize_minimize_button.hide(window)
            elif hide_button == "all":
                hPyT.all_stuffs.hide(window)
            else:
                hPyT.maximize_minimize_button.unhide(window)
                hPyT.all_stuffs.unhide(window)
        if disable_maximize_button is not None:
            hPyT.maximize_button.disable(window) \
                if disable_maximize_button \
                else hPyT.maximize_button.enable(window)
        if disable_minimize_button is not None:
            hPyT.minimize_button.disable(window) \
                if disable_minimize_button \
                else hPyT.minimize_button.enable(window)

    if win32material:
        if boarder_type is not None:
            match boarder_type:
                case "rectangular": boarder_type \
                    = win32material.BORDERTYPE.RECTANGULAR
                case "smallround": boarder_type \
                    = win32material.BORDERTYPE.SMALLROUND
                case "round": boarder_type \
                    = win32material.BORDERTYPE.ROUND
            win32material.SetWindowBorder(tools.get_hwnd(window), boarder_type)


def _process_event(dark: bool) -> None:
    """Handle registered callback functions

    * `dark`: Wether it is dark mode
    """
    for func, args in _callback_events.items():
        try:  # Prevent detection thread from crashing
            func(dark, *args)
        except Exception as exc:
            traceback.print_exception(exc)


def _callback(theme: str) -> None:
    """Callback function that is triggered when a system theme is switched.
    Valid only if the theme mode is set to Follow System

    * `theme`: theme name
    """
    global SYSTEM_DARK_MODE
    SYSTEM_DARK_MODE = theme == "Dark"
    if _color_mode == "system":
        _process_event(SYSTEM_DARK_MODE)


if darkdetect:
    threading.Thread(target=lambda: darkdetect.listener(
        _callback), daemon=True).start()
