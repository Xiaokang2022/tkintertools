"""Support for RGB codes"""

import statistics
import typing

from ..animation import controllers
from . import colormap

RGB = tuple[int, int, int]


def contrast(
    rgb: RGB,
    /,
    channel: tuple[bool, bool, bool] = (True, True, True),
) -> RGB:
    """
    Get a contrasting color of a color

    * `rgb`: a tuple, RGB codes
    * `channel`: three color channels
    """
    return tuple(map(lambda x: x[1] * (256-x[0]), zip(rgb, channel)))


def convert(
    first: RGB,
    second: RGB,
    rate: float,
    *,
    channel: tuple[bool, bool, bool] = (True, True, True),
) -> RGB:
    """
    Convert one color to another proportionally

    * `first`: first color
    * `second`: second color
    * `rate`: conversion rate
    * `channel`: three color channels
    """
    return tuple(first[i] + round((second[i]-first[i])*rate*v) for i, v in enumerate(channel))


def blend(
    colors: list[RGB],
    *,
    weights: list[tuple] | None = None
) -> RGB:
    """
    Mix colors by weight

    * `colors`: color list
    * `weights`: weight list
    """
    colors = zip(*colors)
    if weights is None:  # Same weights
        return tuple(map(lambda x: round(statistics.mean(x)), colors))
    _total = sum(weights)
    weights = tuple(map(lambda x: x/_total, weights))  # Different weights
    return tuple(round(sum(map(lambda x: x[0]*x[1], zip(c, weights)))) for c in colors)


def gradient(
    first: RGB,
    second: RGB,
    count: int,
    rate: float = 1,
    *,
    channels: tuple[bool, bool, bool] = (True, True, True),
    contoller: typing.Callable[[float], float] = controllers.flat,
) -> list[RGB]:
    """
    Get a list of color gradients from one color to another proportionally

    * `first`: first color
    * `second`: second color
    * `count`: number of gradients
    * `rate`: conversion rate
    * `channels`: three color channels
    * `controller`: control function
    """
    rgb_list: list[RGB] = []
    delta = tuple(rate * (j-i) * k for i, j, k in zip(first, second, channels))
    for x in (contoller(i/count) for i in range(count)):
        rgb_list.append(tuple(c + round(x*r) for c, r in zip(first, delta)))
    return rgb_list


def _str_to_rgba(__c: str, *, refer: str) -> RGB:
    """Experimental: Convert color strings(RGBA) to RGB codes"""
    hex, a = divmod(int(__c[1:], 16), 256)
    hex, b = divmod(hex, 256)
    r, g = divmod(hex, 256)
    refer_rgb = str_to_rgb(refer)
    return convert((r, g, b), refer_rgb, 1 - a/255)


def str_to_rgb(__c: str, /) -> RGB:
    """Convert color strings to RGB codes"""
    if __c.startswith("#"):  # HEX
        hex, b = divmod(int(__c[1:], 16), 256)
        r, g = divmod(hex, 256)
        return r, g, b
    return colormap.name_to_rgb(__c)


def rgb_to_str(rgb: RGB) -> str:
    """Convert RGB codes to color strings"""
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


def _str_to_hex(
    __color: str,
    /,
    *,
    reverse: bool = False,
    add: int = 0
) -> int:
    """
    Convert color strings to hexadecimal integers

    * `__color`: color string
    * `reverse`: Whether to reverse RGB to BGR
    * `add`: added value of the decimal RGB code
    """
    rgb = str_to_rgb(__color)
    tup = tuple(value >> 8 for value in rgb)
    for i in reversed(tup) if reverse else tup:
        add <<= 8
        add += i
    return add
