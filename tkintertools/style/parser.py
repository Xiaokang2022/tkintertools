"""
Parse the style file path and get it

### Structure of theme folder

```
theme/
  ├─theme01_name/
  │   ├─container01_name.json
  │   ├─container02_name.json
  │   ├─ ...
  │   ├─widget01_name/
  │   │   ├─component01_name.extra.json
  │   │   ├─component02_name.extra.json
  │   │   └─ ...
  │   ├─widget02_name/
  │   └─ ...
  ├─theme02_name/
  └─ ...
```

### Structure of `container_name.json`

```json
{
    "arg01": "value01",
    "arg02": "value02",
    ...
}
```

### Structure of `component_name.extra.json`

```json
{
    "state01": {
        "arg01": "color",
        "arg02": "color",
        ...
    },
    "state02": {
        ...
    },
    ...
}
```
"""

import functools
import inspect
import json
import pathlib
import typing

from ..core import containers, virtual
from . import manager

__all__ = [
    "BUILTIN_THEME_FOLDER",
    "set_theme",
    "get_theme_folder_path",
    "get_theme_map",
    "get",
    "write",
    "clear_cache",
]

BUILTIN_THEME_FOLDER: pathlib.Path = pathlib.Path(
    __file__).parent.parent / "theme"

_theme_folder_path: pathlib.Path = BUILTIN_THEME_FOLDER

_theme_map: dict[typing.Literal["dark", "light"], str] = {
    "dark": "Dark", "light": "Light"}


def set_theme(
    *,
    light: str | None = None,
    dark: str | None = None,
    folder: str | pathlib.Path | None = None,
) -> None:
    """
    Set the path to the theme file used by the current program

    * `light`: the name of the theme of the light theme
    * `dark`: the name of the theme of the dark theme
    * `folder`: theme folder path
    """
    global _theme_folder_path
    if folder is not None:
        _theme_folder_path = pathlib.Path(folder)
    if dark is not None:
        _theme_map["dark"] = dark
    if light is not None:
        _theme_map["light"] = light
    if any((light, dark, folder)):
        clear_cache()


def get_theme_folder_path() -> pathlib.Path:
    """Get the theme folder path"""
    return _theme_folder_path


def get_theme_map() -> dict[typing.Literal["dark", "light"], str]:
    """Get the theme map"""
    return _theme_map.copy()


def _get_name(obj: "str | virtual.Widget | virtual.Component") -> str | None:
    """Get the name of the object"""
    if obj is None:
        return None
    if getattr(obj, "name", None) is not None:
        if obj.name.startswith("."):  # Special rule
            return obj.__class__.__name__ + obj.name
        return obj.name
    elif inspect.isclass(obj):
        return obj.__name__
    elif not isinstance(obj, str):
        return obj.__class__.__name__
    return obj


@functools.cache
def _get_file(
    path: pathlib.Path,
    widget: str,
    component: str | None = None,
) -> dict[str, dict[str, str]]:
    """
    Get the style file based on the parameters

    The return value of this function is cached, and when the same style file is fetched,
    the data is fetched directly from the cache, unless `clear_cache` is called

    * `path`: path to the style folder
    * `widget`: widget that need to get styles
    * `component`: component that need to get styles
    """
    file_path = (
        path/widget/f"{component}.json") if component else (path/f"{widget}.json")
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as data:
            return json.load(data)
    return {}


def get(
    widget: "str | virtual.Widget | containers.Canvas",
    component: "str | virtual.Component | None" = None,
    *,
    folder: str | pathlib.Path | None = None,
    theme: str | None = None,
) -> dict[str, dict[str, str]] | dict[str, typing.Any]:
    """
    Get style data based on parameters

    * `widget`: widget that need to get styles
    * `component`: component that need to get styles
    * `folder`: path to the theme folder
    * `theme`: path to the style folder
    """
    if folder is None:
        folder = pathlib.Path(_theme_folder_path)
    if theme is None:
        theme = _theme_map[manager.get_color_mode()]
    widget_name = _get_name(widget)
    component_name = _get_name(component)
    return _get_file(folder / theme, widget_name, component_name)


def write(
    style: dict[str, dict[str, str]] | dict[str, typing.Any],
    widget: "str | virtual.Widget",
    component: "str | virtual.Component | None" = None,
    *,
    folder: str | pathlib.Path,
    theme: str = "MyTheme",
) -> None:
    """
    Write style data to file

    * `style`: style data dict
    * `widget`: widget that need to get styles
    * `component`: component that need to get styles
    * `folder`: path to the theme folder
    * `theme`: path to the style folder
    """
    widget_name = _get_name(widget)
    component_name = _get_name(component)
    if component_name is None:
        file_path = pathlib.Path(folder)/theme/f"{widget_name}.json"
    else:
        file_path = pathlib.Path(folder)/theme / \
            widget_name/f"{component_name}.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(style, file, indent=4)


def clear_cache() -> None:
    """Clear cache of function `_get_file`"""
    return _get_file.cache_clear()
