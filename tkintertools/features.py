"""All standard Features"""

import tkinter
import types
import typing

from . import constants, core


class NoFeature(core.Feature):
    """"""


class OnTouch(core.Feature):
    """"""

    def _touch(self, event: tkinter.Event) -> bool:
        """"""
        if self.master.shape.detect((event.x, event.y)):
            if self._state in ("hover", "click"):
                return False
            self._state = "hover"
            self.master.shape.configure(fill="#E5F1FB", outline="#288CDB")
            return True
        else:
            self._state = "normal"
            self.master.shape.configure(fill="#E1E1E1", outline="#C0C0C0")
            return False


class Command(core.Feature):
    """"""

    def __init__(
        self,
        *,
        command: typing.Callable,
    ) -> None:
        core.Feature.__init__(self)
        self._command: typing.Callable = command

    def _click(self, event: tkinter.Event) -> bool:
        """"""
        if self._state == "hover":
            self._state = "click"
            self.master.shape.configure(fill="#CCE4F7", outline="#4884B4")
            return True
        return False

    def _release(self, event: tkinter.Event) -> bool:
        """"""
        if self.master.shape.detect((event.x, event.y)):
            self._state = "hover"
            self.master.shape.configure(fill="#E5F1FB", outline="#288CDB")
            self._command()
            return True
        return False


class Button(Command, OnTouch):
    """"""

    def _touch(self, event: tkinter.Event) -> bool:
        """"""
        if self.master.shape.detect((event.x, event.y)):
            if self._state in ("hover", "click"):
                return False
            self._state = "hover"
            self.master.shape.configure(fill="#E5F1FB", outline="#288CDB")
            self.master.master.configure(cursor="hand2")
            return True
        else:
            self._state = "normal"
            self.master.shape.configure(fill="#E1E1E1", outline="#C0C0C0")
            return False


class UnderLine(Button):
    """"""

    def _touch(self, event: tkinter.Event) -> bool:
        """"""
        if self.master.shape.detect((event.x, event.y)):
            if self._state in ("hover", "click"):
                return False
            self._state = "hover"
            self.master.text.configure(underline=True, fill="blue")
            return True
        else:
            self._state = "normal"
            self.master.text.configure(underline=False, fill="black")
            return False

    def _click(self, event: tkinter.Event) -> bool:
        """"""
        if self._state == "hover":
            self._state = "click"
            self.master.text.configure(fill="purple")
            return True
        return False

    def _release(self, event: tkinter.Event) -> bool:
        """"""
        if self.master.shape.detect((event.x, event.y)):
            self._state = "hover"
            self._command()
            return True
        return False
