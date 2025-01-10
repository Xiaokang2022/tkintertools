"""Some functions about HSL codes."""

from __future__ import annotations

__all__ = [
    "contrast",
    "transition",
    "blend",
    "gradient",
]

import collections.abc
import math
import statistics

from ..animation import controllers


def contrast(
    value: tuple[float, float, float],
    /,
    *,
    channels: tuple[bool, bool, bool] = (True, True, True),
) -> tuple[float, float, float]:
    """Get the contrasting color of a HSL code.

    * `value`: a HSL code
    * `channels`: three color channels
    """
    max_value = math.tau, 1, 1
    return tuple(m-v if c else v for c, m, v in zip(channels, max_value, value))


def transition(
    first: tuple[float, float, float],
    second: tuple[float, float, float],
    rate: float,
    *,
    channels: tuple[bool, bool, bool] = (True, True, True),
) -> tuple[float, float, float]:
    """Transition one color to another proportionally.

    * `first`: the first HSL code
    * `second`: the second HSL code
    * `rate`: transition rate
    * `channels`: three color channels
    """
    return tuple(first[i] + (second[i]-first[i]) * rate * v for i, v in enumerate(channels))


def blend(
    *values: tuple[float, float, float],
    weights: list[float] | None = None,
) -> tuple[float, float, float]:
    """Mix colors by weight.

    * `values`: HSL codes
    * `weights`: weight list, default value indicates the same weights
    """
    colors = zip(*values)

    if weights is None:  # Same weights
        return tuple(map(statistics.mean, colors))

    total = sum(weights)
    weights = tuple(map(lambda x: x/total, weights))  # Different weights

    return tuple(sum(map(lambda x: x[0]*x[1], zip(c, weights))) for c in colors)


def gradient(
    first: tuple[float, float, float],
    second: tuple[float, float, float],
    count: int,
    rate: float = 1,
    *,
    channels: tuple[bool, bool, bool] = (True, True, True),
    contoller: collections.abc.Callable[[float], float] = controllers.linear,
) -> list[tuple[float, float, float]]:
    """Get a list of color gradients from one color to another proportionally.

    * `first`: the first HSL code
    * `second`: the second HSL code
    * `count`: the number of gradients
    * `rate`: transition rate
    * `channels`: three color channels
    * `controller`: control function
    """
    rgb_list: list[tuple[float, float, float]] = []
    delta = tuple(rate * (j-i) * k for i, j, k in zip(first, second, channels))

    for x in (contoller(i/count) for i in range(count)):
        rgb_list.append(tuple(c + x*r for c, r in zip(first, delta)))

    return rgb_list
