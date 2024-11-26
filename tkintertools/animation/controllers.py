"""Standard control functions

Definition of control function:

```python
def f(t: float) -> float: ...
```

* t: 0% ~ 100%, indicates the percentage of time
* return value: Any real number, represents a multiple of the cardinality of the animation

The built-in control functions are:

* `flat`: speed remains the same
* `smooth`: speed is slow first, then fast and then slow
* `rebound`: before the end, displacement will bounce off a bit
"""

from __future__ import annotations

__all__ = [
    "controller_generator",
    "flat",
    "smooth",
    "rebound",
]

import collections.abc
import functools
import math
import warnings


def _map_t(start: float, end: float) -> collections.abc.Callable[[float], float]:
    """Map parameters in any range between 0 and 1

    * `start`: the first value of the parameter of control function
    * `end`: the last value of the parameter of control function
    """
    def _mapper(t: float) -> float:
        return start + t * (end-start)

    return _mapper


def _map_y(
    base_function: collections.abc.Callable[[float], float],
    end: float,
) -> collections.abc.Callable[[float], float]:
    """Map the final return value to 1

    * `base_function`: base function
    * `end`: the last value of the parameter of control function
    """
    @functools.wraps(base_function)
    def _mapper(t: float) -> float:
        return base_function(t) / base_function(end)

    return _mapper


def controller_generator(
    base_function: collections.abc.Callable[[float], float],
    start: float,
    end: float,
    *,
    map_y: bool = True,
) -> collections.abc.Callable[[float], float]:
    """Generator of control functions

    Modify the generic function to a control function suitable for animation

    * `base_function`: base function
    * `start`: the first value of the parameter of control function
    * `end`: the last value of the parameter of control function
    * `map_y`: whether map the final return value to 1

    For example:

    * Before modifying: $y = 2\\sint, 0 <= t <= \\pi/2$
    * After modifying: $y = \\sin\\frac{\\pi}{2}t, 0 <= t <= 1$
    """
    if map_y:
        if math.isclose(base_function(end), 0, abs_tol=1e-9):
            warnings.warn(
                "The end value of the base function is too close to 0, "
                "which may cause the result control function to be "
                "inaccurate or even throw an error.", UserWarning, 2)

        @functools.wraps(base_function)
        def _mapper(t: float) -> float:
            return _map_y(base_function, end)(_map_t(start, end)(t))
    else:
        @functools.wraps(base_function)
        def _mapper(t: float) -> float:
            return base_function(_map_t(start, end)(t))

    return _mapper


def flat(t: float) -> float:
    """Flat animation: speed remains the same"""
    return t


def smooth(t: float) -> float:
    """Smooth animation: speed is slow first, then fast and then slow"""
    return (1 - math.cos(t*math.pi)) / 2


def rebound(t: float) -> float:
    """Rebound animation: before the end, displacement will bounce off a bit"""
    return controller_generator(math.sin, 0, (math.pi+1) / 2)(t)
