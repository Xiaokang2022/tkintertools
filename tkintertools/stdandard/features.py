"""All standard Features"""

import tkinter
import typing

from .. import core


class NoFeature(core.Feature):
    """"""


class Label(core.Feature):
    """"""

    def _move_none(self, event: tkinter.Event) -> bool:
        if flag := self.widget.shape.detect((event.x, event.y)):
            if self.widget.state == "normal":
                self.widget.update("hover")
        else:
            if self.widget.state != "normal":
                self.widget.update("normal")
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
        if flag := self.widget.shape.detect((event.x, event.y)):
            if self.widget.state == "normal":
                self.widget.update("hover")
                self.widget.master.configure(cursor="hand2")
        else:
            if self.widget.state != "normal":
                self.widget.update("normal")
        return flag

    def _move_left(self, event: tkinter.Event) -> bool:
        return self._move_none(event)

    def _move_center(self, event: tkinter.Event) -> bool:
        return self._move_none(event)

    def _move_right(self, event: tkinter.Event) -> bool:
        return self._move_none(event)

    def _click_left(self, event: tkinter.Event) -> bool:
        if flag := self.widget.state == "hover":
            self.widget.update("click")
        return flag

    def _release_left(self, event: tkinter.Event) -> bool:
        """"""
        if self.widget.shape.detect((event.x, event.y)):
            if self.widget.state == "click":
                self.widget.update("hover")
                if self._command is not None:
                    self._command(*self._args)
                return True
        elif self.widget.state == "click":
            self.widget.update("normal")
            self.widget.master.configure(cursor="arrow")
        return False


class UnderLine(Button):
    """"""

    def _move_none(self, event: tkinter.Event) -> bool:
        if flag := self.widget.shape.detect((event.x, event.y)):
            if self.widget.state == "normal":
                self.widget.update("hover")
                self.widget.master.configure(cursor="hand2")
        else:
            if self.widget.state != "normal":
                self.widget.update("normal")
        return flag

    def _click_left(self, event: tkinter.Event) -> bool:
        if flag := self.widget.state == "hover":
            self.widget.update("click")
        return flag

    def _release_left(self, event: tkinter.Event) -> bool:
        """"""
        if self.widget.shape.detect((event.x, event.y)):
            if self.widget.state == "click":
                self.widget.update("hover")
                if self._command is not None:
                    self._command(*self._args)
                return True
        elif self.widget.state == "click":
            self.widget.update("normal")
            self.widget.master.configure(cursor="arrow")
        return False


class Highlight(Button):
    """"""

    def _move_none(self, event: tkinter.Event) -> bool:
        if flag := self.widget.shape.detect((event.x, event.y)):
            if self.widget.state == "normal":
                self.widget.update("hover")
                self.widget.master.configure(cursor="hand2")
        else:
            if self.widget.state != "normal":
                self.widget.update("normal")
        return flag

    def _click_left(self, event: tkinter.Event) -> bool:
        if flag := self.widget.state == "hover":
            self.widget.update("click")
        return flag

    def _release_left(self, event: tkinter.Event) -> bool:
        """"""
        if self.widget.shape.detect((event.x, event.y)):
            if self.widget.state == "click":
                self.widget.update("hover")
                if self._command is not None:
                    self._command(*self._args)
                return True
        elif self.widget.state == "click":
            self.widget.update("normal")
            self.widget.master.configure(cursor="arrow")
        return False


__all__ = [
    "NoFeature",
    "Label",
    "Button",
    "UnderLine",
    "Highlight",
]
