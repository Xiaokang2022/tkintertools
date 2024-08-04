"""
Default style file

Structure for `theme_name.py`

```python
container_name01: dict[str, str | int] = {
    "attr01": value,
    "attr02": ...,
}

...

widget_name01: dict[str, dict[str, dict[str, str]]] = {
    "component01": {
        "state01": { attr01: "color", attr02: "color", ...},
        "state02": ...,
    },
    "component02": ...,
}

...
```

"""

from . import dark, light

# Imports using "from ... import *" are not recommended here
