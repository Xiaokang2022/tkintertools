"""
Standard Controllers

Controller function: `y = f(t)`

```yaml
Parameter:
    t: float
    0% ~ 100%, indicates the percentage of time.
Return:
    y: float
    Any real number, represents a multiple of 
    the cardinality of the animation.
```
"""

import math
import typing


def mapper_t(start: float, end: float) -> typing.Callable[[float], float]:
    """"""
    delta = end - start

    def mapper(t: float) -> float:
        return start + t * delta

    return mapper


def mapper_y(base_func: typing.Callable[[float], float], end: float) -> typing.Callable[[float], float]:
    """"""
    end_value = base_func(end)

    def mapper(t: float) -> float:
        return base_func(t) / end_value

    return mapper


def controller_generator(base_func: typing.Callable[[float], float], start: float, end: float) -> typing.Callable[[float], float]:
    """"""
    def _wrapper(t: float) -> float:
        """"""
        return mapper_y(base_func, end)(mapper_t(start, end)(t))
    return _wrapper


def flat(t: float) -> float:
    """"""
    return t


def smooth(t: float) -> float:
    """"""
    return (1-math.cos(t*math.pi))/2


def rebound(t: float) -> float:
    """"""
    return controller_generator(math.sin, 0, math.pi/2 + 0.5)(t)
