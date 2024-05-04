"""Support for Animation"""

import tkinter
import typing


class Animation:
    """Base Class"""

    def __init__(
        self,
        ms: int,
        controller: typing.Callable[[float], float],
        *,
        callback: typing.Callable[[float], typing.Any] = None,
        end: typing.Callable[[], typing.Any] = None,
        repeat: int = 0,
        fps: int = 30,
    ) -> None:
        """"""
        self.ms = ms
        self.controller = controller
        self.callback = callback
        self.end = end
        self.repeat = repeat
        self.fps = fps

        self._delay: int = 1000 // fps
        if self._delay <= self.ms:
            self._total, self._leave = divmod(self.ms, self._delay)
        else:
            self._delay = self.ms
            self._total, self._leave = 1, -1
        self._tasks: list[str] = []

    def _wrapper(self, func: typing.Callable[[float], float]) -> typing.Callable[[float], float]:
        """"""
        def wrapper(x: float) -> None:
            func(x)
            if self.end is not None:
                self.end()
            if self.repeat != 0:
                self.repeat -= 1
                self.start()
        return wrapper

    def start(self, *, delay: int = 0) -> None:
        """"""
        self._tasks.clear()
        for i in range(1, self._total+1):
            delay += self._delay + (i < self._leave)
            self._tasks.append(
                tkinter._default_root.after(
                    delay,
                    self._wrapper(
                        self.callback) if i == self._total else self.callback,
                    self.controller(i/self._total)
                )
            )

    def stop(self) -> None:
        """"""
        for task in self._tasks[::-1]:
            tkinter._default_root.after_cancel(task)
