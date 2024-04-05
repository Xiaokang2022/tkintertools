"""Support for theme"""

import inspect
import json
import pathlib
import typing

from .. import _tools, constants, core

__cache: dict[tuple, typing.Any] = {}


def get(widget: "core.Widget | str", folder: str | None = None, theme: str = "theme") -> dict:
    """"""
    if inspect.isclass(widget):
        widget = widget.__name__ + ".json"
    elif not isinstance(widget, str):
        widget = widget.__class__.__name__ + ".json"
    else:
        widget += ".json"

    if value := __cache.get(args := (widget, folder, theme)):
        return value

    if folder is None:
        folder = pathlib.Path(__file__).parent
        theme = "win10" if constants.IS_WIN10 else "win11"
    else:
        folder = pathlib.Path(folder)

    style = "dark" if _tools.is_dark() else "light"

    if pathlib.Path(folder/theme/style).exists():
        with open(folder/theme/style/widget, "r", encoding="utf-8") as data:
            __cache[args] = json.load(data)
    else:
        with open(folder/theme/widget, "r", encoding="utf-8") as data:
            __cache[args] = json.load(data)

    return __cache[args]
