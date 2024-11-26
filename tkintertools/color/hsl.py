"""Support for HSL"""

from __future__ import annotations

__all__ = [
    "contrast",
    "convert",
    "blend",
    "gradient",
    "hsl_to_rgb",
    "hsl2rgb",
    "rgb_to_hsl",
    "rgb2hsl",
]

import collections.abc
import colorsys
import math
import statistics

from ..animation import controllers
from . import rgb

HSL = tuple[float, float, float]
"""
H: Hue, 0.0 ~ 2pi
S: Saturation, 0.0 ~ 1.0
L: Lightness, 0.0 ~ 1.0
"""

MAX = math.tau, 1, 1
"""The maximum value of the HSL code"""


def contrast(hsl: HSL, *, channels: tuple[bool, bool, bool] = (True, True, True)) -> HSL:
    """Get a contrasting color of a color

    * `hsl`: a tuple, HSL codes
    * `channels`: three color channels
    """
    return tuple(map(lambda x: (x[1]-x[2]) if x[0] else x[2], zip(channels, MAX, hsl)))


def convert(
    first: HSL,
    second: HSL,
    rate: float,
    *,
    channels: tuple[bool, bool, bool] = (True, True, True),
) -> HSL:
    """Convert one color to another proportionally

    * `first`: first color
    * `second`: second color
    * `rate`: conversion rate
    * `channels`: three color channels
    """
    return tuple(first[i] + (second[i]-first[i]) * rate * v for i, v in enumerate(channels))


def blend(colors: list[HSL], *, weights: list[float] | None = None) -> HSL:
    """Mix colors by weight

    * `colors`: color list
    * `weights`: weight list
    """
    colors = zip(*colors)

    if weights is None:  # Same weights
        return tuple(map(statistics.mean, colors))

    _total = sum(weights)
    weights = tuple(map(lambda x: x/_total, weights))  # Different weights

    return tuple(sum(map(lambda x: x[0]*x[1], zip(c, weights))) for c in colors)


def gradient(
    first: HSL,
    second: HSL,
    count: int,
    rate: float = 1,
    *,
    channels: tuple[bool, bool, bool] = (True, True, True),
    contoller: collections.abc.Callable[[int | float], int | float] = controllers.flat,
) -> list[HSL]:
    """Get a list of color gradients from one color to another proportionally

    * `first`: first color
    * `second`: second color
    * `count`: number of gradients
    * `rate`: conversion rate
    * `channels`: three color channels
    * `controller`: control function
    """
    rgb_list: list[HSL] = []
    delta = tuple(rate * (j-i) * k for i, j, k in zip(first, second, channels))

    for x in (contoller(i/count) for i in range(count)):
        rgb_list.append(tuple(c + x*r for c, r in zip(first, delta)))

    return rgb_list


def hsl_to_rgb(color: HSL) -> rgb.RGB:
    """Convert HSL to RGB codes"""
    c = colorsys.hls_to_rgb(color[0]/math.tau, color[1], color[2])
    return tuple(round(i*255) for i in c)


hsl2rgb = hsl_to_rgb  # Alias


def rgb_to_hsl(color: rgb.RGB) -> HSL:
    """Convert RGB to HSL codes"""
    c = colorsys.rgb_to_hls(*tuple(i/255 for i in color))
    return c[0]*math.tau, c[1], c[2]


rgb2hsl = rgb_to_hsl  # Alias
