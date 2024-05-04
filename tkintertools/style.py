"""Support for style"""

import functools
import inspect
import json
import pathlib

import darkdetect

from . import core

system_theme_path = pathlib.Path(__file__).parent / "theme"
default_theme_path = pathlib.Path().cwd() / "theme"


def _get_name(obj: "str | core.Widget | core.Component") -> str:
    """"""
    if getattr(obj, "name", None) is not None:
        return obj.name
    elif inspect.isclass(obj):
        return obj.__name__
    elif not isinstance(obj, str):
        return obj.__class__.__name__
    return obj


def _get_file(path: pathlib.Path, widget: str, component: str, dark: bool) -> pathlib.Path | None:
    """"""
    folder = path / widget
    file = folder / f"{component}.json"
    if file.exists():
        return file
    mode = "dark" if dark else "light"
    file = folder / f"{component}.{mode}.json"
    if file.exists():
        return file
    return None


@functools.cache
def _get(widget: str, component: str, path: pathlib.Path, dark: bool) -> "dict[core.State, core.Style]":
    """"""
    for path in set((system_theme_path, default_theme_path, path)):
        if file := _get_file(path, widget, component, dark):
            with open(file, "r", encoding="utf-8") as data:
                return json.load(data)
    return {}


def get(widget: "str | core.Widget", component: "str | core.Component", *, path: str | pathlib.Path = system_theme_path) -> "dict[core.State, core.Style]":
    """"""
    dark_mode = darkdetect.isDark()
    widget_name = _get_name(widget)
    component_name = _get_name(component)
    return _get(widget_name, component_name, pathlib.Path(path), dark_mode)
