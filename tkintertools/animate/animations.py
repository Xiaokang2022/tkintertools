"""Standard animations"""

import typing

from .. import color, core
from . import Animation, controllers


class MoveWidget(Animation):
    """"""

    def __init__(
        self,
        widget: "core.Widget",
        ms: int,
        controller: typing.Callable[[float], float],
        *,
        delta: tuple[float, float] | tuple[float, float, float, float],
        end: typing.Callable[[], typing.Any] = None,
        repeat: int = 0,
        fps: int = 30
    ) -> None:
        if len(delta) == 2:
            x, y = widget.x, widget.y
            dx, dy = delta
        else:
            x, y, *_ = delta
            dx, dy = delta[2] - x, delta[3] - y
        super().__init__(
            ms, controller,
            callback=lambda p: widget.moveto(x+dx*p, y+dy*p),
            end=end, repeat=repeat, fps=fps
        )


class MoveComponent(Animation):
    """"""

    def __init__(
        self,
        component: "core.Component",
        ms: int,
        controller: typing.Callable[[float], float],
        *,
        delta: tuple[float, float] | tuple[float, float, float, float],
        end: typing.Callable[[], typing.Any] = None,
        repeat: int = 0,
        fps: int = 30
    ) -> None:
        if len(delta) == 2:
            x, y = component.x, component.y
            dx, dy = delta
        else:
            x, y, *_ = delta
            dx, dy = delta[2] - x, delta[3] - y
        super().__init__(
            ms, controller,
            callback=lambda p: component.moveto(x+dx*p, y+dy*p),
            end=end, repeat=repeat, fps=fps
        )


class Gradient(Animation):
    """"""

    def __init__(
        self,
        canvas: "core.Canvas",
        item: int,
        argname: str,
        ms: int,
        *,
        delta: str | tuple[str, str],
        end: typing.Callable[[], typing.Any] = None,
        repeat: int = 0,
        fps: int = 30
    ) -> None:
        if isinstance(delta, str):
            delta = [canvas.itemcget(item, argname), delta]
            if delta[0] == "":
                delta[0] = "black"
            if delta[1] == "":
                delta[1] = "black"
        super().__init__(ms, None, end=end, repeat=repeat, fps=fps)
        self._color_list = color.color(delta, seqlength=self._total)
        self.controller = lambda t: round(t*self._total) - 1
        self.callback = lambda p: canvas.itemconfigure(
            item, **{argname: self._color_list[p]})


class ScaleFontSize(Animation):
    """"""

    def __init__(
        self,
        text: "core.Text",
        ms: int,
        *,
        delta: float | tuple[float, float],
        end: typing.Callable[[], typing.Any] = None,
        repeat: int = 0,
        fps: int = 30
    ) -> None:
        self._text = text
        delta = -abs(delta)
        if not isinstance(delta, tuple):
            delta = text.font.cget("size"), delta-text.font.cget("size")
        super().__init__(
            ms, controllers.flat,
            callback=lambda p: self._scale(round(delta[0] + delta[1]*p)),
            end=end, repeat=repeat, fps=fps
        )

    def _scale(self, size: int) -> None:
        """"""
        self._text.font.config(size=size)
        self._text.update()
