"""All standard Features"""

import tkinter
import typing

from . import core


class NoFeature(core.Feature):
    """"""


class Label(core.Feature):
    """"""

    def _move_none(self, event: tkinter.Event) -> bool:
        if flag := self.master.shape.detect((event.x, event.y)):
            if self.master.state == "normal":
                self.master.state = "hover"
        else:
            if self.master.state != "normal":
                self.master.state = "normal"
        return flag


class Button(core.Feature):
    """"""

    def __init__(
        self,
        *,
        command: typing.Callable,
        args: tuple = (),
    ) -> None:
        """"""
        core.Feature.__init__(self)
        self._command: typing.Callable = command
        self._args: tuple = args

    def _move_none(self, event: tkinter.Event) -> bool:
        if flag := self.master.shape.detect((event.x, event.y)):
            if self.master.state == "normal":
                self.master.state = "hover"
                self.master.master.configure(cursor="hand2")
        else:
            if self.master.state != "normal":
                self.master.state = "normal"
        return flag

    def _move_left(self, event: tkinter.Event) -> bool:
        return self._move_none(event)

    def _move_center(self, event: tkinter.Event) -> bool:
        return self._move_none(event)

    def _move_right(self, event: tkinter.Event) -> bool:
        return self._move_none(event)

    def _click_left(self, event: tkinter.Event) -> bool:
        if flag := self.master.state == "hover":
            self.master.state = "click"
        return flag

    def _release_left(self, event: tkinter.Event) -> bool:
        """"""
        if self.master.shape.detect((event.x, event.y)):
            if self.master.state == "click":
                self.master.state = "hover"
                if self._command is not None:
                    self._command(*self._args)
                return True
        elif self.master.state == "click":
            self.master.state = "normal"
            self.master.master.configure(cursor="arrow")
        return False


class UnderLine(Button):
    """"""

    def _move_none(self, event: tkinter.Event) -> bool:
        if flag := self.master.shape.detect((event.x, event.y)):
            if self.master.state == "normal":
                self.master.state = "hover"
                self.master.text.configure(underline=True)
                self.master.master.configure(cursor="hand2")
        else:
            if self.master.state != "normal":
                self.master.state = "normal"
                self.master.text.configure(underline=False)
        return flag

    def _click_left(self, event: tkinter.Event) -> bool:
        if flag := self.master.state == "hover":
            self.master.state = "click"
        return flag

    def _release_left(self, event: tkinter.Event) -> bool:
        """"""
        if self.master.shape.detect((event.x, event.y)):
            if self.master.state == "click":
                self.master.state = "hover"
                if self._command is not None:
                    self._command(*self._args)
                return True
        elif self.master.state == "click":
            self.master.state = "normal"
            self.master.master.configure(cursor="arrow")
        return False


class Highlight(Button):
    """"""

    def _move_none(self, event: tkinter.Event) -> bool:
        if flag := self.master.shape.detect((event.x, event.y)):
            if self.master.state == "normal":
                self.master.state = "hover"
                self.master.master.configure(cursor="hand2")
        else:
            if self.master.state != "normal":
                self.master.state = "normal"
        return flag

    def _click_left(self, event: tkinter.Event) -> bool:
        if flag := self.master.state == "hover":
            self.master.state = "click"
        return flag

    def _release_left(self, event: tkinter.Event) -> bool:
        """"""
        if self.master.shape.detect((event.x, event.y)):
            if self.master.state == "click":
                self.master.state = "hover"
                if self._command is not None:
                    self._command(*self._args)
                return True
        elif self.master.state == "click":
            self.master.state = "normal"
            self.master.master.configure(cursor="arrow")
        return False


__all__ = [
    "NoFeature",
    "Label",
    "Button",
    "UnderLine",
    "Highlight",
]
