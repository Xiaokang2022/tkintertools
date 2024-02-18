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
            if self._state == "normal":
                self._state = "hover"
                self.master.shape.configure(fill="#E5F1FB", outline="#288CDB")
        else:
            if self._state != "normal":
                self._state = "normal"
                self.master.shape.configure(fill="#E1E1E1", outline="#C0C0C0")
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
            if self._state == "normal":
                self._state = "hover"
                self.master.shape.configure(fill="#E5F1FB", outline="#288CDB")
                self.master.master.configure(cursor="hand2")
        else:
            if self._state != "normal":
                self._state = "normal"
                self.master.shape.configure(fill="#E1E1E1", outline="#C0C0C0")
        return flag

    def _move_left(self, event: tkinter.Event) -> bool:
        return self._move_none(event)

    def _move_center(self, event: tkinter.Event) -> bool:
        return self._move_none(event)

    def _move_right(self, event: tkinter.Event) -> bool:
        return self._move_none(event)

    def _click_left(self, event: tkinter.Event) -> bool:
        if flag := self._state == "hover":
            self._state = "click"
            self.master.shape.configure(fill="#CCE4F7", outline="#4884B4")
        return flag

    def _release_left(self, event: tkinter.Event) -> bool:
        """"""
        if self.master.shape.detect((event.x, event.y)):
            if self._state == "click":
                self._state = "hover"
                self.master.shape.configure(fill="#E5F1FB", outline="#288CDB")
                self._command(*self._args)
                return True
        elif self._state == "click":
            self._state = "normal"
            self.master.shape.configure(fill="#E1E1E1", outline="#C0C0C0")
            self.master.master.configure(cursor="arrow")
        return False


class UnderLine(Button):
    """"""

    def _move_none(self, event: tkinter.Event) -> bool:
        if flag := self.master.shape.detect((event.x, event.y)):
            if self._state == "normal":
                self._state = "hover"
                self.master.text.configure(underline=True, fill="blue")
                self.master.master.configure(cursor="hand2")
        else:
            if self._state != "normal":
                self._state = "normal"
                self.master.text.configure(underline=False, fill="black")
        return flag

    def _click_left(self, event: tkinter.Event) -> bool:
        if flag := self._state == "hover":
            self._state = "click"
            self.master.text.configure(fill="purple")
        return flag

    def _release_left(self, event: tkinter.Event) -> bool:
        """"""
        if self.master.shape.detect((event.x, event.y)):
            if self._state == "click":
                self._state = "hover"
                self._command(*self._args)
                return True
        elif self._state == "click":
            self._state = "normal"
            self.master.master.configure(cursor="arrow")
        return False


class Highlight(Button):
    """"""

    def _move_none(self, event: tkinter.Event) -> bool:
        if flag := self.master.shape.detect((event.x, event.y)):
            if self._state == "normal":
                self._state = "hover"
                self.master.text.configure(fill="#1F1F1F")
                self.master.master.configure(cursor="hand2")
        else:
            if self._state != "normal":
                self._state = "normal"
                self.master.text.configure(fill="grey")
        return flag

    def _click_left(self, event: tkinter.Event) -> bool:
        if flag := self._state == "hover":
            self._state = "click"
            self.master.text.configure(fill="black")
        return flag

    def _release_left(self, event: tkinter.Event) -> bool:
        """"""
        if self.master.shape.detect((event.x, event.y)):
            if self._state == "click":
                self._state = "hover"
                self._command(*self._args)
                return True
        elif self._state == "click":
            self._state = "normal"
            self.master.master.configure(cursor="arrow")
        return False


__all__ = [
    "NoFeature",
    "Label",
    "Button",
    "UnderLine",
    "Highlight",
]
