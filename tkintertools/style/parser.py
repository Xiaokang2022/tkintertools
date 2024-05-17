"""Parse the style file path and get it"""

import functools
import inspect
import json
import pathlib

from .. import core
from . import theme

system_theme_path = pathlib.Path(__file__).parent.parent / "theme"
default_theme_path = pathlib.Path().cwd() / "theme"


def _get_name(obj: "str | core.Widget | core.Component") -> str:
    """Get the name of the object"""
    if getattr(obj, "name", None) is not None:
        if obj.name.startswith("."):  # Special rule
            return obj.__class__.__name__ + obj.name
        return obj.name
    elif inspect.isclass(obj):
        return obj.__name__
    elif not isinstance(obj, str):
        return obj.__class__.__name__
    return obj


def _get_path(path: pathlib.Path, widget: str, component: str, dark: bool) -> pathlib.Path | None:
    """
    Obtain the path to the style file based on the parameters

    * `path`: path to the theme folder
    * `widget`: widget that need to get styles
    * `component`: component that need to get styles
    * `dark`: whether it is in dark mode
    """
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
def _get_file(widget: str, component: str, path: pathlib.Path, dark: bool) -> "dict[str, dict[str, str]]":
    """
    Get the style file based on the parameters

    The return value of this function is cached, and when the same style file is fetched,
    the data is fetched directly from the cache

    * `widget`: widget that need to get styles
    * `component`: component that need to get styles
    * `path`: path to the theme folder
    * `dark`: whether it is in dark mode
    """
    for path in set((system_theme_path, default_theme_path, path)):
        if file := _get_path(path, widget, component, dark):
            with open(file, "r", encoding="utf-8") as data:
                return json.load(data)
    return {}


def get(widget: "str | core.Widget", component: "str | core.Component", *, path: str | pathlib.Path = system_theme_path) -> "dict[str, dict[str, str]]":
    """
    Get style data based on parameters

    * `widget`: widget that need to get styles
    * `component`: component that need to get styles
    * `path`: path to the theme folder, which is the built-in theme path by default

    The order in which the theme folder looks for paths is as follows:

    system_theme_path > relative path > custom path
    """
    widget_name = _get_name(widget)
    component_name = _get_name(component)
    return _get_file(widget_name, component_name, pathlib.Path(path), theme.DARK_MODE)
