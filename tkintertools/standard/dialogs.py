"""All standard Dialogs"""

import tkinter
import tkinter.colorchooser as colorchooser
import typing

from .. import core


class Message:
    """"""

    def __init__(
        self,
        message: str | None = None,
        detail: str | None = None,
        *,
        title: str | None = None,
        icon: typing.Literal["error", "info", "question", "warning"] = "info",
        type: typing.Literal["abortretryignore", "ok", "okcancel",
                             "retrycancel", "yesno", "yesnocancel"] = "ok",
        default: str | None = None,
        master: tkinter.Misc | None = None,
        command: typing.Callable[[typing.Literal[
            "abort", "retry", "ignore", "ok", "cancel", "yes", "no"]], typing.Any] | None = None,
    ) -> None:
        """"""
        if master is None:
            master: tkinter.Misc = tkinter._default_root
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
        if type is not None:
            args += ["-type", type]
        if default is not None:
            args += ["-default", default]
        value = master.call("tk_messageBox", "-parent", master, *args)
        if command is not None:
            command(value)


class ColorChooser:
    """"""

    def __init__(
        self,
        *,
        title: str | None = None,
        color: str | None = None,
        master: tkinter.Misc | None = None,
        command: typing.Callable[[str], typing.Any] | None = None,
    ) -> None:
        """"""
        color: tuple[tuple[int, int, int] | None, str | None] = colorchooser.askcolor(
            parent=master, title=title, initialcolor=color)
        if command is not None and color[0] is not None:
            command(color[1])


class FontChooser:
    """"""

    def __init__(
        self,
        *,
        title: str | None = None,
        font: str | None = None,
        master: tkinter.Misc | None = None,
        command: typing.Callable[[str], typing.Any] | None = None,
    ) -> None:
        """"""
        if master is None:
            master: tkinter.Misc = tkinter._default_root
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


class PopUp(core.Dialog):
    """"""


class ToolTip(PopUp):
    """"""
