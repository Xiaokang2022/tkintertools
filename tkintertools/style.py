"""Support for style"""

import functools
import inspect
import json
import pathlib

from . import _tools, core

system_theme_path = pathlib.Path(__file__).parent / "theme"
default_theme_path = pathlib.Path().cwd() / "theme"
dark_mode = _tools.is_dark()


def get_path(path: str | pathlib.Path) -> pathlib.Path:
    """"""
    if isinstance(path, str):
        path = pathlib.Path(path)
    if path.exists():
        return path
    return system_theme_path


def get_name(obj: "str | core.Widget | core.Component") -> str:
    """"""
    if getattr(obj, "name", None) is not None:
        return obj.name
    elif inspect.isclass(obj):
        return obj.__name__
    elif not isinstance(obj, str):
        return obj.__class__.__name__
    return obj


def get_file(path: pathlib.Path, widget: str, component: str) -> pathlib.Path:
    """"""
    folder = path / widget
    file = folder / f"{component}.json"
    if file.exists():
        return file
    mode = "dark" if dark_mode else "light"
    return folder / f"{component}.{mode}.json"


@functools.cache
def get(widget: "str | core.Widget", component: "str | core.Component", *, path: str | pathlib.Path = default_theme_path) -> "dict[core.State, core.Style]":
    """"""
    file = get_file(get_path(path), get_name(widget), get_name(component))
    if not file.exists():
        return {}
    with open(file, "r", encoding="utf-8") as data:
        return json.load(data)
