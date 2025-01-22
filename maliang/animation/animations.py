"""Base and standard animation classes.

The animation base class can be inherited or called directly. Other standard
animation classes are best used by direct calls, rather than inheritance.
"""

from __future__ import annotations

__all__ = [
    "Animation",
    "MoveWindow",
    "MoveTkWidget",
    "MoveWidget",
    "MoveElement",
    "MoveItem",
    "GradientTkWidget",
    "GradientItem",
    "ScaleFontSize",
]

import collections.abc
import tkinter
import typing
import warnings

from ..color import convert, rgb
from ..core import configs, containers, virtual
from . import controllers


class Animation:
    """Base animation class."""

    def __init__(
        self,
        duration: int,
        command: collections.abc.Callable[[float], typing.Any],
        *,
        controller: collections.abc.Callable[[float], float] = controllers.linear,
        end: collections.abc.Callable[[], typing.Any] | None = None,
        fps: int = 30,
        repeat: int = 0,
        repeat_delay: int = 0,
        derivation: bool = False,
    ) -> None:
        """
        * `duration`: duration of the animation, in milliseconds
        * `command`: callback function, which will be called once per frame
        * `controller`: a function that controls the animation process
        * `end`: end function, which is called once at the end of the animation
        * `fps`: frame rate of the animation
        * `repeat`: number of repetitions of the animation
        * `repeat_delay`: length of the delay before the animation repeats
        * `derivation`: whether the callback function is derivative
        """
        self.command = command
        self.controller = controller
        self.end = end
        self.repeat = repeat
        self.repeat_delay = repeat_delay
        self.derivation = derivation

        self._delay: int = 1000 // fps
        self._tasks: list[str] = []
        self._count: int = repeat

        if self._delay <= duration:
            self._total_frames, self._leave_ms = divmod(duration, self._delay)
        else:
            self._delay, self._total_frames, self._leave_ms = duration, 1, 0

    @property
    def active(self) -> bool:
        """Returns the active state of the animation."""
        return bool(self._tasks)

    @property
    def count(self) -> int:
        """Returns the number of loops remaining."""
        return self._count

    def _repeat(self) -> None:
        """Processing of the number of repetitions."""
        self._tasks.clear()

        if self._count != 0:
            self._count -= 1
            if task := self.start(delay=self.repeat_delay):
                self._tasks.append(task)
        else:
            self._count = self.repeat

    @typing.overload
    def start(self) -> None: ...

    @typing.overload
    def start(self, *, delay: int) -> str: ...

    def start(self, *, delay: int = 0) -> str | None:
        """Start the animation.

        * `delay`: length of the delay before the animation starts
        """
        if delay > 0:
            return configs.Env.root.after(delay, self.start)

        delay, last_percentage = 0, 0

        for i in range(1, self._total_frames + 1):
            delay += self._delay + (i < self._leave_ms)
            percentage = self.controller(i / self._total_frames)
            self._tasks.append(configs.Env.root.after(
                delay, self.command, percentage - last_percentage))

            if self.derivation:
                last_percentage = percentage

        if self.end is not None:
            self._tasks.append(configs.Env.root.after(delay, self.end))

        self._tasks.append(configs.Env.root.after(delay, self._repeat))

        return None

    @typing.overload
    def stop(self) -> None: ...

    @typing.overload
    def stop(self, *, delay: int) -> str: ...

    def stop(self, *, delay: int = 0) -> str | None:
        """Stop the animation.

        * `delay`: length of the delay before the animation stops
        """
        if delay > 0:
            return configs.Env.root.after(delay, self.stop)

        while self._tasks:
            configs.Env.root.after_cancel(self._tasks.pop())

        self._count = self.repeat

        return None

    def skip(self, count: int = 1) -> None:
        """Skip some loops.

        * `count`: count of skipping
        """
        self._count = max(self._count-count, 0)


class MoveWindow(Animation):
    """Animation of moving the window."""

    def __init__(
        self,
        window: tkinter.Tk | tkinter.Toplevel | containers.Tk | containers.Toplevel,
        offset: tuple[float, float],
        duration: int,
        *,
        controller: collections.abc.Callable[[float], float] = controllers.linear,
        end: collections.abc.Callable[[], typing.Any] | None = None,
        fps: int = 30,
        repeat: int = 0,
        repeat_delay: int = 0,
    ) -> None:
        """
        * `window`: the window to be moved
        * `offset`: relative offset of the coordinates
        * `duration`: duration of the animation, in milliseconds
        * `controller`: a function that controls the animation process
        * `end`: end function, which is called once at the end of the animation
        * `fps`: frame rate of the animation
        * `repeat`: number of repetitions of the animation
        * `repeat_delay`: length of the delay before the animation repeats
        """
        window.update()
        x0, y0, dx, dy = window.winfo_x(), window.winfo_y(), *offset

        if isinstance(window, (containers.Tk, containers.Toplevel)):
            def callback(p) -> None:
                window.geometry(position=(round(x0+dx*p), round(y0+dy*p)))
        else:
            def callback(p) -> None:
                window.wm_geometry(f"+{round(x0+dx*p)}+{round(y0+dy*p)}")

        Animation.__init__(
            self, duration, callback, controller=controller, end=end, fps=fps,
            repeat=repeat, repeat_delay=repeat_delay,
        )


class MoveTkWidget(Animation):
    """Animation of moving `tkinter.Widget`."""

    def __init__(
        self,
        widget: tkinter.Widget,
        offset: tuple[float, float],
        duration: int,
        *,
        controller: collections.abc.Callable[[float], float] = controllers.linear,
        end: collections.abc.Callable[[], typing.Any] | None = None,
        fps: int = 30,
        repeat: int = 0,
        repeat_delay: int = 0,
    ) -> None:
        """
        * `widget`: the `tkinter.Widget` to be moved
        * `offset`: relative offset of the coordinates
        * `duration`: duration of the animation, in milliseconds
        * `controller`: a function that controls the animation process
        * `end`: end function, which is called once at the end of the animation
        * `fps`: frame rate of the animation
        * `repeat`: number of repetitions of the animation
        * `repeat_delay`: length of the delay before the animation repeats
        """
        if not widget.place_info():
            warnings.warn(
                "The tkinter widget is not laid out by Place.", UserWarning, 2)

        widget.update()
        x0, y0, dx, dy = widget.winfo_x(), widget.winfo_y(), *offset

        Animation.__init__(
            self, duration, lambda p: widget.place(x=x0+dx*p, y=y0+dy*p),
            controller=controller, end=end, fps=fps, repeat=repeat,
            repeat_delay=repeat_delay,
        )


class MoveWidget(Animation):
    """Animation of moving `virtual.Widget`."""

    def __init__(
        self,
        widget: virtual.Widget,
        offset: tuple[float, float],
        duration: int,
        *,
        controller: collections.abc.Callable[[float], float] = controllers.linear,
        end: collections.abc.Callable[[], typing.Any] | None = None,
        fps: int = 30,
        repeat: int = 0,
        repeat_delay: int = 0,
    ) -> None:
        """
        * `widget`: the `virtual.Widget` to be moved
        * `offset`: relative offset of the coordinates
        * `duration`: duration of the animation, in milliseconds
        * `controller`: a function that controls the animation process
        * `end`: end function, which is called once at the end of the animation
        * `fps`: frame rate of the animation
        * `repeat`: number of repetitions of the animation
        * `repeat_delay`: length of the delay before the animation repeats
        """
        Animation.__init__(
            self, duration, lambda p: widget.move(offset[0]*p, offset[1]*p),
            controller=controller, end=end, fps=fps, repeat=repeat,
            repeat_delay=repeat_delay, derivation=True,
        )


class MoveElement(Animation):
    """Animation of moving `virtual.Element`."""

    def __init__(
        self,
        element: virtual.Element,
        offset: tuple[float, float],
        duration: int,
        *,
        controller: collections.abc.Callable[[float], float] = controllers.linear,
        end: collections.abc.Callable[[], typing.Any] | None = None,
        fps: int = 30,
        repeat: int = 0,
        repeat_delay: int = 0,
    ) -> None:
        """
        * `element`: the `virtual.Element` to be moved
        * `offset`: relative offset of the coordinates
        * `duration`: duration of the animation, in milliseconds
        * `controller`: a function that controls the animation process
        * `end`: end function, which is called once at the end of the animation
        * `fps`: frame rate of the animation
        * `repeat`: number of repetitions of the animation
        * `repeat_delay`: length of the delay before the animation repeats
        """
        Animation.__init__(
            self, duration, lambda p: element.move(offset[0]*p, offset[1]*p),
            controller=controller, end=end, fps=fps, repeat=repeat,
            repeat_delay=repeat_delay, derivation=True,
        )


class MoveItem(Animation):
    """Animation of moving a item of `tkinter.Canvas`."""

    def __init__(
        self,
        canvas: tkinter.Canvas | containers.Canvas,
        item: int,
        offset: tuple[float, float],
        duration: int,
        *,
        controller: collections.abc.Callable[[float], float] = controllers.linear,
        end: collections.abc.Callable[[], typing.Any] | None = None,
        fps: int = 30,
        repeat: int = 0,
        repeat_delay: int = 0,
    ) -> None:
        """
        * `canvas`: an instance of `tkinter.Canvas` that contains the item
        * `item`: the item to be moved
        * `offset`: relative offset of the coordinates
        * `duration`: duration of the animation, in milliseconds
        * `controller`: a function that controls the animation process
        * `end`: end function, which is called once at the end of the animation
        * `fps`: frame rate of the animation
        * `repeat`: number of repetitions of the animation
        * `repeat_delay`: length of the delay before the animation repeats
        """
        Animation.__init__(
            self, duration, lambda p: canvas.move(
                item, offset[0]*p, offset[1]*p),
            controller=controller, end=end, fps=fps, repeat=repeat,
            repeat_delay=repeat_delay, derivation=True,
        )


class GradientTkWidget(Animation):
    """Animation of making the color of `tkinter.Widget` to be gradient."""

    def __init__(
        self,
        widget: tkinter.Widget,
        parameter: str,
        colors: tuple[str, str],
        duration: int,
        *,
        controller: collections.abc.Callable[[float], float] = controllers.linear,
        end: collections.abc.Callable[[], typing.Any] | None = None,
        fps: int = 30,
        repeat: int = 0,
        repeat_delay: int = 0,
        derivation: bool = False,
    ) -> None:
        """
        * `widget`: the `tkinter.Widget` whose color is to be gradient
        * `parameter`: parameter name of widget that is to be modified in color
        * `colors`: a tuple of the initial and ending colors
        * `duration`: duration of the animation, in milliseconds
        * `controller`: a function that controls the animation process
        * `end`: end function, which is called once at the end of the animation
        * `fps`: frame rate of the animation
        * `repeat`: number of repetitions of the animation
        * `repeat_delay`: length of the delay before the animation repeats
        * `derivation`: whether the callback function is derivative
        """
        if not all(colors):
            raise ValueError(f"Null characters ({colors}) cannot be parsed!")

        c1, c2 = convert.str_to_rgb(colors[0]), convert.str_to_rgb(colors[1])

        Animation.__init__(
            self, duration, lambda p: widget.configure(
                {parameter: convert.rgb_to_hex(rgb.transition(c1, c2, p))}),
            controller=controller, end=end, fps=fps, repeat=repeat,
            repeat_delay=repeat_delay, derivation=derivation,
        )


class GradientItem(Animation):
    """Animation of making the color of canvas item to be gradient."""

    def __init__(
        self,
        canvas: tkinter.Canvas | containers.Canvas,
        item: int,
        parameter: str,
        colors: tuple[str, str],
        duration: int,
        *,
        controller: collections.abc.Callable[[float], float] = controllers.linear,
        end: collections.abc.Callable[[], typing.Any] | None = None,
        fps: int = 30,
        repeat: int = 0,
        repeat_delay: int = 0,
        derivation: bool = False,
    ) -> None:
        """
        * `canvas`: an instance of `tkinter.Canvas` that contains the item
        * `item`: item whose color is to be gradient
        * `parameter`: parameter name of item that is to be modified in color
        * `colors`: a tuple of the initial and ending colors
        * `duration`: duration of the animation, in milliseconds
        * `controller`: a function that controls the animation process
        * `end`: end function, which is called once at the end of the animation
        * `fps`: frame rate of the animation
        * `repeat`: number of repetitions of the animation
        * `repeat_delay`: length of the delay before the animation repeats
        * `derivation`: whether the callback function is derivative
        """
        if not all(colors):
            raise ValueError(f"Null characters ({colors}) cannot be parsed!")

        c1, c2 = convert.str_to_rgb(colors[0]), convert.str_to_rgb(colors[1])

        Animation.__init__(
            self, duration, lambda p: canvas.itemconfigure(
                item, {parameter: convert.rgb_to_hex(rgb.transition(c1, c2, p))}),
            controller=controller, end=end, fps=fps, repeat=repeat,
            repeat_delay=repeat_delay, derivation=derivation,
        )


class ScaleFontSize(Animation):
    """Animation of scaling the font size of `virtual.Text`."""

    @typing.overload
    def __init__(
        self,
        text: virtual.Text,
        sizes: float,
        duration: int,
        *,
        controller: collections.abc.Callable[[float], float] = controllers.linear,
        end: collections.abc.Callable[[], typing.Any] | None = None,
        fps: int = 30,
        repeat: int = 0,
        repeat_delay: int = 0,
        derivation: bool = False,
    ) -> None: ...

    @typing.overload
    def __init__(
        self,
        text: virtual.Text,
        sizes: tuple[float, float],
        duration: int,
        *,
        controller: collections.abc.Callable[[float], float] = controllers.linear,
        end: collections.abc.Callable[[], typing.Any] | None = None,
        fps: int = 30,
        repeat: int = 0,
        repeat_delay: int = 0,
        derivation: bool = False,
    ) -> None: ...

    def __init__(
        self,
        text: virtual.Text,
        sizes: float | tuple[float, float],
        duration: int,
        *,
        controller: collections.abc.Callable[[float], float] = controllers.linear,
        end: collections.abc.Callable[[], typing.Any] | None = None,
        fps: int = 30,
        repeat: int = 0,
        repeat_delay: int = 0,
        derivation: bool = False,
    ) -> None:
        """
        * `text`: an instance of `virtual.Text` that needs to be scaled
        * `sizes`: a tuple of the initial and ending sizes or target font size
        * `duration`: duration of the animation, in milliseconds
        * `controller`: a function that controls the animation process
        * `end`: end function, which is called once at the end of the animation
        * `fps`: frame rate of the animation
        * `repeat`: number of repetitions of the animation
        * `repeat_delay`: length of the delay before the animation repeats
        * `derivation`: whether the callback function is derivative
        """
        if isinstance(sizes, (int, float)):
            sizes = -abs(sizes)
            sizes = text.font.cget("size"), sizes - text.font.cget("size")
        else:
            sizes = -abs(sizes[0]), -abs(sizes[1])
            sizes = sizes[0], sizes[1] - sizes[0]

        Animation.__init__(
            self, duration, lambda p: (
                text.font.config(size=round(sizes[0] + sizes[1]*p)),
                text.update()),
            controller=controller, end=end, fps=fps, repeat=repeat,
            repeat_delay=repeat_delay, derivation=derivation,
        )
