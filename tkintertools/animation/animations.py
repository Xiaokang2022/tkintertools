"""
Standard animation classes

The built-in basic animation classes are: `MoveTkWidget`, `MoveWidget`,
`MoveComponent`, `MoveItem`, `GradientTkWidget`, `GradientItem`, `ScaleFontSize`
"""

import numbers
import tkinter
import typing
import warnings

from ..color import rgb
from ..core import virtual
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
    """Animation base class"""

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
        * `ms`: duration of the animation, in milliseconds
        * `controller`: control functions that determine the course of the
        entire animation movement
        * `callback`: callback function, which will be called once per frame,
        with the parameter being the percentage of the current animation
        progress
        * `end`: ending function, which is called once at the end of the
        animation
        * `repeat`: number of repetitions of the entire animation process
        * `fps`: the FPS of the animation
        * `derivation`: whether the callback function is derivative
        """
        self.ms = ms
        self.controller = controller
        self.callback = callback
        self.end = end
        self.repeat = repeat
        self.fps = fps
        self.derivation = derivation

        self._tasks: list[str] = []
        self._delay: int = 1000 // fps

        if self._delay <= self.ms:
            self._total, self._leave = divmod(self.ms, self._delay)
        else:
            self._delay, self._total, self._leave = self.ms, 1, -1

    def _wrapper(
        self,
        func: typing.Callable[[float], float],
    ) -> typing.Callable[[float], float]:
        """
        Make the ending function call correctly

        * `func`: the callback function to be wrapped
        """
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
        Start the animation

        * `delay`: length of the delay before the animation starts, in
        milliseconds 
        """
        self._tasks.clear()
        last_percentage = 0

        for i in range(1, self._total+1):
            delay += self._delay + (i < self._leave)
            percentage = self.controller(i/self._total)
            task = tkinter.Misc.after(
                tkinter._default_root, delay,
                self._wrapper(
                    self.callback) if i == self._total else self.callback,
                percentage - last_percentage
            )
            self._tasks.append(task)

            if self.derivation:
                last_percentage = percentage

    def stop(self) -> None:
        """Stop the animation"""
        for task in self._tasks[::-1]:
            tkinter.Misc.after_cancel(tkinter._default_root, task)


class MoveTkWidget(Animation):
    """Animation of moving `tkinter.Widget`"""

    def __init__(
        self,
        widget: tkinter.Widget,
        ms: int,
        offset: tuple[float, float],
        *,
        controller: typing.Callable[[float], float] = controllers.flat,
        end: typing.Callable[[], typing.Any] | None = None,
        repeat: int = 0,
        fps: int = 30,
    ) -> None:
        """
        * `widget`: tkinter widget to be moved
        * `ms`: duration of the animation, in milliseconds
        * `offset`: relative offset of the coordinates
        * `controller`: control functions that determine the course of the
        entire animation movement
        * `end`: ending function, which is called once at the end of the
        animation
        * `repeat`: number of repetitions of the entire animation process
        * `fps`: the FPS of the animation
        """
        if not widget.place_info():
            warnings.warn(
                "tkinter widget is not laid out by Place.", UserWarning, 2)

        widget.update_idletasks()
        x0, y0, dx, dy = widget.winfo_x(), widget.winfo_y(), *offset

        Animation.__init__(
            self, ms, controller,
            callback=lambda p: widget.place(x=x0+dx*p, y=y0+dy*p),
            end=end, repeat=repeat, fps=fps,
        )


class MoveWidget(Animation):
    """Animation of moving `Widget`"""

    def __init__(
        self,
        widget: "virtual.Widget",
        ms: int,
        offset: tuple[float, float],
        *,
        controller: typing.Callable[[float], float] = controllers.flat,
        end: typing.Callable[[], typing.Any] | None = None,
        repeat: int = 0,
        fps: int = 30,
    ) -> None:
        """
        * `widget`: widget to be moved
        * `ms`: duration of the animation, in milliseconds
        * `offset`: relative offset of the coordinates
        * `controller`: control functions that determine the course of the
        entire animation movement
        * `end`: ending function, which is called once at the end of the
        animation
        * `repeat`: number of repetitions of the entire animation process
        * `fps`: the FPS of the animation
        """
        dx, dy = offset

        Animation.__init__(
            self, ms, controller,
            callback=lambda p: widget.move(dx*p, dy*p),
            end=end, repeat=repeat, fps=fps, derivation=True,
        )


class MoveComponent(Animation):
    """Animation of moving `Component`"""

    def __init__(
        self,
        component: "virtual.Component",
        ms: int,
        offset: tuple[float, float],
        *,
        controller: typing.Callable[[float], float] = controllers.flat,
        end: typing.Callable[[], typing.Any] | None = None,
        repeat: int = 0,
        fps: int = 30,
    ) -> None:
        """
        * `component`: component to be moved
        * `ms`: duration of the animation, in milliseconds
        * `offset`: relative offset of the coordinates
        * `controller`: control functions that determine the course of the
        entire animation movement
        * `end`: ending function, which is called once at the end of the
        animation
        * `repeat`: number of repetitions of the entire animation process
        * `fps`: the FPS of the animation
        """
        dx, dy = offset

        Animation.__init__(
            self, ms, controller,
            callback=lambda p: component.move(dx*p, dy*p),
            end=end, repeat=repeat, fps=fps, derivation=True,
        )


class MoveItem(Animation):
    """Animation of moving a item"""

    def __init__(
        self,
        canvas: tkinter.Canvas,
        item: int,
        ms: int,
        offset: tuple[float, float],
        *,
        controller: typing.Callable[[float], float] = controllers.flat,
        end: typing.Callable[[], typing.Any] | None = None,
        repeat: int = 0,
        fps: int = 30,
    ) -> None:
        """
        * `canvas`: an instance of `tkinter.Canvas` that contains the item
        * `item`: the item to be moved
        * `ms`: duration of the animation, in milliseconds
        * `offset`: relative offset of the coordinates
        * `controller`: control functions that determine the course of the
        entire animation movement
        * `end`: ending function, which is called once at the end of the
        animation
        * `repeat`: number of repetitions of the entire animation process
        * `fps`: the FPS of the animation
        """
        dx, dy = offset

        Animation.__init__(
            self, ms, controller,
            callback=lambda p: canvas.move(item, dx*p, dy*p),
            end=end, repeat=repeat, fps=fps, derivation=True,
        )


class GradientTkWidget(Animation):
    """Animation that makes color of `tkinter.Widget` gradient"""

    def __init__(
        self,
        widget: tkinter.Widget,
        parameter: str,
        ms: int,
        colors: tuple[str, str],
        *,
        controller: typing.Callable[[float], float] = controllers.flat,
        end: typing.Callable[[], typing.Any] | None = None,
        repeat: int = 0,
        fps: int = 30,
        derivation: bool = False,
    ) -> None:
        """
        * `widget`: tkinter widget whose color is to be gradient
        * `parameter`: parameter name of the part of the item that needs to be
        modified in color
        * `ms`: duration of the animation, in milliseconds
        * `colors`: a tuple of the initial and ending colors
        * `controller`: control functions that determine the course of the
        entire animation movement
        * `end`: ending function, which is called once at the end of the
        animation
        * `repeat`: number of repetitions of the entire animation process
        * `fps`: the FPS of the animation
        * `derivation`: whether the callback function is derivative
        """
        if not all(colors):
            raise ValueError(f"Null characters ({colors}) cannot be parsed!")

        rgb1, rgb2 = rgb.str_to_rgb(colors[0]), rgb.str_to_rgb(colors[1])

        Animation.__init__(
            self, ms, controller,
            callback=lambda p: widget.configure(
                **{parameter: rgb.rgb_to_str(rgb.convert(rgb1, rgb2, p))}),
            end=end, repeat=repeat, fps=fps, derivation=derivation,
        )


class GradientItem(Animation):
    """Animation that makes color of canvas item gradient"""

    def __init__(
        self,
        canvas: tkinter.Canvas,
        item: int,
        parameter: str,
        ms: int,
        colors: tuple[str, str],
        *,
        controller: typing.Callable[[float], float] = controllers.flat,
        end: typing.Callable[[], typing.Any] | None = None,
        repeat: int = 0,
        fps: int = 30,
        derivation: bool = False,
    ) -> None:
        """
        * `canvas`: an instance of `tkinter.Canvas` that contains the item
        * `item`: item whose color is to be gradient
        * `parameter`: parameter name of the part of the item that needs to be
        modified in color
        * `ms`: duration of the animation, in milliseconds
        * `colors`: a tuple of the initial and ending colors
        * `controller`: control functions that determine the course of the
        entire animation movement
        * `end`: ending function, which is called once at the end of the
        animation
        * `repeat`: number of repetitions of the entire animation process
        * `fps`: the FPS of the animation
        * `derivation`: whether the callback function is derivative
        """
        if not all(colors):
            raise ValueError(f"Null characters ({colors}) cannot be parsed!")

        rgb1, rgb2 = rgb.str_to_rgb(colors[0]), rgb.str_to_rgb(colors[1])

        Animation.__init__(
            self, ms, controller,
            callback=lambda p: canvas.itemconfigure(item, **{
                parameter: rgb.rgb_to_str(rgb.convert(rgb1, rgb2, p))}),
            end=end, repeat=repeat, fps=fps, derivation=derivation,
        )


class ScaleFontSize(Animation):
    """Animation of scaling the font size"""

    def __init__(
        self,
        text: "virtual.Text",
        ms: int,
        sizes: tuple[float, float] | float,
        *,
        controller: typing.Callable[[float], float] = controllers.flat,
        end: typing.Callable[[], typing.Any] | None = None,
        repeat: int = 0,
        fps: int = 30,
        derivation: bool = False,
    ) -> None:
        """
        * `text`: an instance of `virtual.Text` that needs to be scaled in font
        size
        * `ms`: duration of the animation, in milliseconds
        * `sizes`: a tuple of the initial and ending sizes or target font size
        * `controller`: control functions that determine the course of the
        entire animation movement
        * `end`: ending function, which is called once at the end of the
        animation
        * `repeat`: number of repetitions of the entire animation process
        * `fps`: the FPS of the animation
        * `derivation`: whether the callback function is derivative
        """
        self._text = text

        if isinstance(sizes, numbers.Number):
            sizes = -abs(sizes)
            sizes = text.font.cget("size"), sizes-text.font.cget("size")
        else:
            sizes = -abs(sizes[0]), -abs(sizes[1])
            sizes = sizes[0], sizes[1] - sizes[0]

        Animation.__init__(
            self, ms, controller,
            callback=lambda p: self._scale(round(sizes[0] + sizes[1]*p)),
            end=end, repeat=repeat, fps=fps, derivation=derivation,
        )

    def _scale(self, size: int) -> None:
        """Scale font size"""
        self._text.font.config(size=size)
        self._text.update()
