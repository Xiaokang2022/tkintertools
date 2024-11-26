"""Parse the style file path and get it

Structure of theme folder:

* format of ".py": see tkintertools/theme/__init__.py
* format of ".json":

```
theme/
  ├─theme01_name/
  │   ├─container01_name.json
  │   ├─container02_name.json
  │   ├─ ...
  │   ├─widget01_name.json
  │   ├─widget02_name.json
  │   └─ ...
  ├─theme02_name/
  └─ ...
```

* Structure of `container_name.json`:

```json
{
    "arg01": "value01",
    "arg02": "value02",
    ...
}
```

* Structure of `widget_name.extra.json`:

```json
{
    "component01": {
        "state01": {
            "arg01": "color",
            "arg02": "color",
            ...
        },
        "state02": {
            ...
        },
        ...
    },
    "component02": {
        ...
    },
    ...
}
```

Style files in JSON format must strictly follow the above format, and the missing parts are empty
by default.
"""

from __future__ import annotations

__all__ = [
    "get",
]

import functools
import inspect
import json
import pathlib
import types
import typing

from ..core import configs, containers, virtual
from . import manager


def _get_name(
    obj: str | virtual.Widget | virtual.Component | containers.Canvas | None,
) -> str | None:
    """Get the name of the object"""
    if obj is None:
        return None
    name: str | None = getattr(obj, "name", None)
    if name is not None:
        if inspect.isclass(name):
            name = name.__name__
        elif name.startswith("."):  # Special rule
            name = obj.__class__.__name__ + name
        return name
    if inspect.isclass(obj):
        return obj.__name__
    if not isinstance(obj, str):
        return obj.__class__.__name__
    return obj


@functools.cache
def get_file(
    theme: str | pathlib.Path | types.ModuleType,
    widget: str,
    component: str | None = None,
) -> dict[str, dict[str, str]]:
    """Get the style file based on the parameters

    The return value of this function is cached, and when the same style file is fetched, the data
    is fetched directly from the cache, unless `clear_cache` is called

    * `theme`: a specified theme
    * `widget`: widget that need to get styles
    * `component`: component that need to get styles
    """
    if isinstance(theme, types.ModuleType):
        if hasattr(theme, widget):
            if component is None:
                return getattr(theme, widget)
            return getattr(theme, widget).get(component, {})
    elif (file_path := pathlib.Path(theme)/f"{widget}.json").exists():
        with open(file_path, "r", encoding="utf-8") as data:
            if component is None:
                return json.load(data)
            return json.load(data).get(component, {})
    return {}


def get(
    widget: str | virtual.Widget | containers.Canvas,
    component: str | virtual.Component | None = None,
    *,
    theme: str | pathlib.Path | types.ModuleType | None = None,
) -> dict[str, dict[str, str]] | dict[str, typing.Any]:
    """Get style data based on parameters

    * `widget`: widget that need to get styles
    * `component`: component that need to get styles
    * `theme`: path to the style folder
    """
    if theme is None:
        if manager.get_color_mode() == "dark":
            theme = configs.Theme.dark
        else:
            theme = configs.Theme.light
    return get_file(theme, _get_name(widget), _get_name(component)).copy()
