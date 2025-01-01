"""All standard dialog classes"""

from __future__ import annotations

__all__ = [
    "TkMessage",
    "TkColorChooser",
    "TkFontChooser",
]

import collections.abc
import tkinter
import tkinter.colorchooser
import typing


class TkMessage:
    """Message pop-up"""

    def __init__(
        self,
        message: str | None = None,
        detail: str | None = None,
        *,
        title: str | None = None,
        icon: typing.Literal["error", "info", "question", "warning"] = "info",
        option: typing.Literal["abortretryignore", "ok", "okcancel", "retrycancel", "yesno", "yesnocancel"] = "ok",
        default: typing.Literal["abort", "retry", "ignore", "ok", "cancel", "yes", "no"] | None = None,
        master: tkinter.Tk | None = None,
        command: collections.abc.Callable[[typing.Literal["abort", "retry", "ignore", "ok", "cancel", "yes", "no"]], typing.Any] | None = None,
    ) -> None:
        """
        * `message`: message
        * `detail`: detail message
        * `title`: title of the window
        * `icon`: icon
        * `option`: type of the message pop-up
        * `default`: button where the focus is, default is the leftmost one
        * `master`: parent widget of the window
        * `command`: callback function
        """
        if master is None:
            master = tkinter._get_temp_root()

        args = ["-icon", icon]

        if title is not None:
            args += ["-title", title]
        elif master is not None:
            args += ["-title", master.title()]

        if message is not None:
            args += ["-message", message]
        if detail is not None:
            args += ["-detail", detail]
        if option is not None:
            args += ["-type", option]
        if default is not None:
            args += ["-default", default]

        value = master.call("tk_messageBox", "-parent", master, *args)

        if command is not None:
            command(value)


class TkColorChooser:
    """Color chooser pop-up"""

    def __init__(
        self,
        *,
        title: str | None = None,
        color: str | None = None,
        master: tkinter.Tk | None = None,
        command: collections.abc.Callable[[str], typing.Any] | None = None,
    ) -> None:
        """
        * `title`: title of the window
        * `color`: default color
        * `master`: parent widget of the window
        * `command`: callback function
        """
        colors = tkinter.colorchooser.askcolor(
            initialcolor=color, parent=master, title=title)

        if command is not None and colors[0] is not None:
            command(colors[1])


class TkFontChooser:
    """Font chooser pop-up"""

    def __init__(
        self,
        *,
        title: str | None = None,
        font: str | None = None,
        master: tkinter.Tk | None = None,
        command: collections.abc.Callable[[str], typing.Any] | None = None,
    ) -> None:
        """
        * `title`: title of the window
        * `font`: default font
        * `master`: parent widget of the window
        * `command`: callback function
        """
        if master is None:
            master = tkinter._get_temp_root()

        args = []
        if title is not None:
            args += ["-title", title]
        if font is not None:
            args += ["-font", font]
        if command is not None:
            args += ["-command", master.register(command)]

        master.call("tk", "fontchooser", "configure", "-parent", master, *args)
        master.call("tk", "fontchooser", "show")
