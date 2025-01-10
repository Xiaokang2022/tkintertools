"""Controller generator and standard control functions.

Definition of control function:

```python
def f(t: float) -> float: ...
```

* `t`: 0% ~ 100%, indicates the percentage of time
* return: real number, indicates a multiple of the cardinality of the animation
"""

from __future__ import annotations

__all__ = [
    "generate",
    "linear",
    "smooth",
    "rebound",
    "ease_in",
    "ease_out",
]

import collections.abc
import functools
import math
import typing
import warnings


def _map_t(
    start: float,
    end: float,
) -> collections.abc.Callable[[float], float]:
    """Map parameters in any range between 0 and 1.

    * `start`: the first value of the parameter of the base function
    * `end`: the last value of the parameter of the base function
    """
    def _mapper(t: float) -> float:
        return start + t * (end-start)

    return _mapper


def _map_y(
    base: collections.abc.Callable[[float], float],
    end: float,
) -> collections.abc.Callable[[float], float]:
    """Map the final return value to 1.

    * `base`: base function
    * `end`: the last value of the parameter of the base function
    """
    @functools.wraps(base)
    def _mapper(t: float) -> float:
        return base(t) / base(end)

    return _mapper


@typing.overload
def generate(
    base: collections.abc.Callable[[float], float],
    start: float,
    end: float,
) -> collections.abc.Callable[[float], float]: ...


@typing.overload
def generate(
    base: collections.abc.Callable[[float], float],
    start: float,
    end: float,
    *,
    map_y: typing.Literal[False] = False,
) -> collections.abc.Callable[[float], float]: ...


def generate(
    base: collections.abc.Callable[[float], float],
    start: float,
    end: float,
    *,
    map_y: bool = True,
) -> collections.abc.Callable[[float], float]:
    """Generate a control function from an ordinary mathematical function.

    * `base`: base function, an ordinary mathematical function
    * `start`: the first value of the parameter of the base function
    * `end`: the last value of the parameter of the base function
    * `map_y`: whether map the final return value to 1
    """
    if map_y:
        if math.isclose(base(end), 0, abs_tol=1e-9):
            warnings.warn(
                "The end value of the base function is too close to 0, "
                "which may cause the result control function to be "
                "inaccurate or even throw an error.", UserWarning, 2)

        @functools.wraps(base)
        def _mapper(t: float) -> float:
            return _map_y(base, end)(_map_t(start, end)(t))
    else:
        @functools.wraps(base)
        def _mapper(t: float) -> float:
            return base(_map_t(start, end)(t))

    return _mapper


@typing.overload
def linear(t: int) -> int: ...


@typing.overload
def linear(t: float) -> float: ...


def linear(t: float) -> float:
    """Speed remains the same.

    * `t`: the percentage of time
    """
    return t


def smooth(t: float) -> float:
    """Speed is slow first, then fast and then slow. (slow -> fast -> slow)

    * `t`: the percentage of time
    """
    return (1 - math.cos(t*math.pi)) / 2


def rebound(t: float) -> float:
    """Before the end, displacement will bounce off a bit.

    * `t`: the percentage of time
    """
    return generate(math.sin, 0, (math.pi+1) / 2)(t)


def ease_in(t: float) -> float:
    """Gradually accelerate. (slow -> fast)

    * `t`: the percentage of time
    """
    return generate((lambda x: math.pow(2, 10*x - 10)), 0, 1)(t)


def ease_out(t: float) -> float:
    """Gradually decelerate. (fast -> slow)

    * `t`: the percentage of time
    """
    return generate((lambda x: 1 - math.pow(2, -10*x)), 0, 1)(t)
