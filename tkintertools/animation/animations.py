"""Standard animations"""

import numbers
import tkinter
import typing
import warnings

from ..color import rgb
from ..core import containers, virtual
from . import controllers

__all__ = [
    "Animation",
    "MoveTkWidget",
    "MoveWidget",
    "MoveComponent",
    "MoveItem",
    "GradientTkWidget",
    "GradientItem",
    "ScaleFontSize",
]


class Animation:
    """Base Class for Animation"""

    def __init__(
        self,
        ms: int,
        controller: typing.Callable[[float], float],
        *,
        callback: typing.Callable[[float], typing.Any] | None = None,
        end: typing.Callable[[], typing.Any] | None = None,
        repeat: int = 0,
        fps: int = 30,
        derivation: bool = False,
    ) -> None:
        """
        * `ms`: animation duration
        * `controller`: control function
        * `callback`: callback function, which will be called once per frame,
        and the parameter is the current animation percentage
        * `end`: the function that is called at the end of the animation normally
        * `repeat`: the number of times the entire animation is repeated
        * `fps`: the frame rate of the animation
        * `derivation`: whether the callback function is derivative
        """
        self.ms = ms
        self.controller = controller
        self.callback = callback
        self.end = end
        self.repeat = repeat
        self.fps = fps
        self.derivation = derivation

        self._delay: int = 1000 // fps
        if self._delay <= self.ms:
            self._total, self._leave = divmod(self.ms, self._delay)
        else:
            self._delay = self.ms
            self._total, self._leave = 1, -1
        self._tasks: list[str] = []

    def _wrapper(self, func: typing.Callable[[float], float]) -> typing.Callable[[float], float]:
        """Internal Method: Make the end function call correctly"""
        def wrapper(x: float) -> None:
            func(x)
            if self.end is not None:
                self.end()
            if self.repeat != 0:
                self.repeat -= 1
                self.start()
        return wrapper

    def start(self, *, delay: int = 0) -> None:
        """
        Play the animation

        * `delay`: the delay before the animation starts
        """
        self._tasks.clear()
        last_value: float = 0
        for i in range(1, self._total+1):
            delay += self._delay + (i < self._leave)
            percentage = self.controller(i/self._total)
            self._tasks.append(
                tkinter.Misc.after(
                    tkinter._default_root, delay,
                    self._wrapper(
                        self.callback) if i == self._total else self.callback,
                    percentage - last_value
                )
            )
            if self.derivation:
                last_value = percentage

    def stop(self) -> None:
        """Stop the animation"""
        for task in self._tasks[::-1]:
            tkinter.Misc.after_cancel(tkinter._default_root, task)


class MoveTkWidget(Animation):
    """Animation of moving a `tkinter.Widget`"""

    def __init__(
        self,
        widget: tkinter.Widget,
        ms: int,
        delta: tuple[float, float],
        *,
        controller: typing.Callable[[float], float] = controllers.flat,
        end: typing.Callable[[], typing.Any] | None = None,
        repeat: int = 0,
        fps: int = 30,
    ) -> None:
        """
        * `widget`: tkinter widget that is moved
        * `ms`: animation duration
        * `delta`: displacement, (dx, dy)
        * `controller`: control function
        * `end`: the function that is called at the end of the animation normally
        * `repeat`: the number of times the entire animation is repeated
        * `fps`: the frame rate of the animation
        """
        if not widget.place_info():
            warnings.warn("Canvas is not laid out by Place")
        x0, y0, dx, dy = widget.winfo_x(), widget.winfo_y(), *delta
        Animation.__init__(
            self, ms, controller,
            callback=lambda k: widget.place(x=x0+dx*k, y=y0+dy*k),
            end=end, repeat=repeat, fps=fps,
        )


class MoveWidget(Animation):
    """Animation of moving a `Widget`"""

    def __init__(
        self,
        widget: "virtual.Widget",
        ms: int,
        delta: tuple[float, float],
        *,
        controller: typing.Callable[[float], float] = controllers.flat,
        end: typing.Callable[[], typing.Any] | None = None,
        repeat: int = 0,
        fps: int = 30,
    ) -> None:
        """
        * `widget`: widget that is moved
        * `ms`: animation duration
        * `delta`: displacement, (dx, dy)
        * `controller`: control function
        * `end`: the function that is called at the end of the animation normally
        * `repeat`: the number of times the entire animation is repeated
        * `fps`: the frame rate of the animation
        """
        dx, dy = delta
        Animation.__init__(
            self, ms, controller,
            callback=lambda k: widget.move(dx*k, dy*k),
            end=end, repeat=repeat, fps=fps, derivation=True,
        )


class MoveComponent(Animation):
    """Animation of moving a `Component`"""

    def __init__(
        self,
        component: "virtual.Component",
        ms: int,
        delta: tuple[float, float],
        *,
        controller: typing.Callable[[float], float] = controllers.flat,
        end: typing.Callable[[], typing.Any] | None = None,
        repeat: int = 0,
        fps: int = 30,
    ) -> None:
        """
        * `component`: component that is moved
        * `ms`: animation duration
        * `delta`: displacement, (dx, dy)
        * `controller`: control function
        * `end`: the function that is called at the end of the animation normally
        * `repeat`: the number of times the entire animation is repeated
        * `fps`: the frame rate of the animation
        """
        dx, dy = delta
        Animation.__init__(
            self, ms, controller,
            callback=lambda k: component.move(dx*k, dy*k),
            end=end, repeat=repeat, fps=fps, derivation=True,
        )


class MoveItem(Animation):
    """Animation of moving a item"""

    def __init__(
        self,
        canvas: "containers.Canvas",
        item: int,
        ms: int,
        delta: tuple[float, float],
        *,
        controller: typing.Callable[[float], float] = controllers.flat,
        end: typing.Callable[[], typing.Any] | None = None,
        repeat: int = 0,
        fps: int = 30,
    ) -> None:
        """
        * `canvas`: canvas object to which the item belongs
        * `item`: item that need to be moved
        * `ms`: animation duration
        * `delta`: displacement, (dx, dy)
        * `controller`: control function
        * `end`: the function that is called at the end of the animation normally
        * `repeat`: the number of times the entire animation is repeated
        * `fps`: the frame rate of the animation
        """
        dx, dy = delta
        Animation.__init__(
            self, ms, controller,
            callback=lambda k: canvas.move(item, dx*k, dy*k),
            end=end, repeat=repeat, fps=fps, derivation=True,
        )


class GradientTkWidget(Animation):
    """Animation for color gradients"""

    def __init__(
        self,
        widget: tkinter.Widget,
        option: str,
        ms: int,
        delta: tuple[str, str],
        *,
        controller: typing.Callable[[float], float] = controllers.flat,
        end: typing.Callable[[], typing.Any] | None = None,
        repeat: int = 0,
        fps: int = 30,
        derivation: bool = False,
    ) -> None:
        """
        * `widget`: tkinter widget
        * `option`: parameter name of the part of the item that needs to be modified in color
        * `ms`: animation duration
        * `delta`: (start color, stop color)
        * `controller`: control function
        * `end`: the function that is called at the end of the animation normally
        * `repeat`: the number of times the entire animation is repeated
        * `fps`: the frame rate of the animation
        * `derivation`: whether the callback function is derivative
        """
        if not all(delta):
            raise ValueError("Null characters cannot be parsed")
        Animation.__init__(
            self, ms, controller,
            callback=lambda p: widget.configure(
                **{option: rgb.rgb_to_str(rgb.convert(rgb.str_to_rgb(delta[0]), rgb.str_to_rgb(delta[1]), p))}),
            end=end, repeat=repeat, fps=fps, derivation=derivation,
        )


class GradientItem(Animation):
    """Animation for color gradients"""

    def __init__(
        self,
        canvas: "containers.Canvas",
        item: int,
        option: str,
        ms: int,
        delta: tuple[str, str],
        *,
        controller: typing.Callable[[float], float] = controllers.flat,
        end: typing.Callable[[], typing.Any] | None = None,
        repeat: int = 0,
        fps: int = 30,
        derivation: bool = False,
    ) -> None:
        """
        * `canvas`: canvas object to which the item belongs
        * `item`: item that need to be modified in color
        * `option`: parameter name of the part of the item that needs to be modified in color
        * `ms`: animation duration
        * `delta`: (start color, stop color)
        * `controller`: control function
        * `end`: the function that is called at the end of the animation normally
        * `repeat`: the number of times the entire animation is repeated
        * `fps`: the frame rate of the animation
        * `derivation`: whether the callback function is derivative
        """
        if not all(delta):
            raise ValueError("Null characters cannot be parsed")
        Animation.__init__(
            self, ms, controller,
            callback=lambda p: canvas.itemconfigure(
                item, **{option: rgb.rgb_to_str(rgb.convert(
                    rgb.str_to_rgb(delta[0]), rgb.str_to_rgb(delta[1]), p))}),
            end=end, repeat=repeat, fps=fps, derivation=derivation,
        )


class ScaleFontSize(Animation):
    """Animation for scaling the font size"""

    def __init__(
        self,
        text: "virtual.Text",
        ms: int,
        delta: float | tuple[float, float],
        *,
        controller: typing.Callable[[float], float] = controllers.flat,
        end: typing.Callable[[], typing.Any] | None = None,
        repeat: int = 0,
        fps: int = 30,
        derivation: bool = False,
    ) -> None:
        """
        * `text`: the text to which the font belongs
        * `ms`: animation duration
        * `delta`: target font size or (start size, end size)
        * `controller`: control function
        * `end`: the function that is called at the end of the animation normally
        * `repeat`: the number of times the entire animation is repeated
        * `fps`: the frame rate of the animation
        * `derivation`: whether the callback function is derivative
        """
        self._text = text
        if isinstance(delta, numbers.Number):
            delta = -abs(delta)
            delta = text.font.cget("size"), delta-text.font.cget("size")
        else:
            delta = -abs(delta[0]), -abs(delta[1])
            delta = delta[0], delta[1] - delta[0]
        Animation.__init__(
            self, ms, controller,
            callback=lambda p: self._scale(round(delta[0] + delta[1]*p)),
            end=end, repeat=repeat, fps=fps, derivation=derivation,
        )

    def _scale(self, size: int) -> None:
        """Scale font size"""
        self._text.font.config(size=size)
        self._text.update()
