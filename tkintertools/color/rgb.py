"""Some functions about RGB codes."""

from __future__ import annotations

__all__ = [
    "contrast",
    "transition",
    "blend",
    "gradient",
]

import collections.abc
import statistics

from ..animation import controllers


def contrast(
    value: tuple[int, int, int],
    /,
    *,
    channels: tuple[bool, bool, bool] = (True, True, True),
) -> tuple[int, int, int]:
    """Get the contrasting color of a RGB code.

    * `value`: a RGB code
    * `channels`: three color channels
    """
    return tuple(255-v if c else v for v, c in zip(value, channels))


def transition(
    first: tuple[int, int, int],
    second: tuple[int, int, int],
    rate: float,
    *,
    channels: tuple[bool, bool, bool] = (True, True, True),
) -> tuple[int, int, int]:
    """Transition one color to another proportionally.

    * `first`: the first RGB code
    * `second`: the second RGB code
    * `rate`: transition rate
    * `channels`: three color channels
    """
    return tuple(first[i] + round((second[i]-first[i]) * rate * v) for i, v in enumerate(channels))


def blend(
    *values: tuple[int, int, int],
    weights: list[float] | None = None,
) -> tuple[int, int, int]:
    """Mix colors by weight.

    * `values`: RGB codes
    * `weights`: weight list, default value indicates the same weights
    """
    colors = zip(*values)

    if weights is None:  # Same weights
        return tuple(map(lambda x: round(statistics.mean(x)), colors))

    total = sum(weights)
    weights = tuple(map(lambda x: x/total, weights))  # Different weights

    return tuple(round(sum(map(lambda x: x[0]*x[1], zip(c, weights)))) for c in colors)


def gradient(
    first: tuple[int, int, int],
    second: tuple[int, int, int],
    count: int,
    rate: float = 1,
    *,
    channels: tuple[bool, bool, bool] = (True, True, True),
    contoller: collections.abc.Callable[[float], float] = controllers.linear,
) -> list[tuple[int, int, int]]:
    """Get a list of color gradients from one color to another proportionally.

    * `first`: the first RGB code
    * `second`: the second RGB code
    * `count`: the number of gradients
    * `rate`: transition rate
    * `channels`: three color channels
    * `controller`: control function
    """
    rgb_list: list[tuple[int, int, int]] = []
    delta = tuple(rate * (j-i) * k for i, j, k in zip(first, second, channels))

    for x in (contoller(i/count) for i in range(count)):
        rgb_list.append(tuple(c + round(x*r) for c, r in zip(first, delta)))

    return rgb_list
