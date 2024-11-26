"""Default style data

Base structure for `theme_name.py`:

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

It is not mandatory for the variable to be a constant, it is enough to conform to the above format,
and the missing style will be empty by default and will not affect the operation of the program.
"""
