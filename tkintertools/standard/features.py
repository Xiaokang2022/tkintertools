"""All standard Features"""

import tkinter
import typing

from ..animation import animations
from ..core import virtual

__all__ = [
    "Label",
    "Button",
    "Underline",
    "Highlight",
    "Switch",
    "CheckButton",
    "RadioButton",
    "ProgressBar",
    "Entry",
]


class Label(virtual.Feature):
    """"""

    def _move_none(self, event: tkinter.Event) -> bool:
        if flag := self.widget._shapes[0].detect(event.x, event.y):
            self.widget.master._trigger_config.update(cursor="arrow")
            if self.widget.state != "hover":
                self.widget.update("hover")
        else:
            if self.widget.state != "normal":
                self.widget.update("normal")
        return flag


class Button(virtual.Feature):
    """"""

    def __init__(
        self,
        widget: virtual.Widget,
        *,
        command: typing.Callable | None = None,
        args: tuple = (),
    ) -> None:
        """"""
        virtual.Feature.__init__(self, widget)
        self._command: typing.Callable = command
        self._args: tuple = args

    def _move_none(self, event: tkinter.Event) -> bool:
        if flag := self.widget._shapes[0].detect(event.x, event.y):
            self.widget.master._trigger_config.update(cursor="hand2")
            if self.widget.state == "normal":
                self.widget.update("hover")
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

    def _click_left(self, _: tkinter.Event) -> bool:
        if flag := self.widget.state == "hover":
            self.widget.update("active")
        return flag

    def _release_left(self, event: tkinter.Event) -> bool:
        """"""
        if flag := self.widget._shapes[0].detect(event.x, event.y):
            if self.widget.state == "active":
                self.widget.update("hover")
                if self._command is not None:
                    self._command(*self._args)
        return flag


class Underline(Button):
    """"""

    def _move_none(self, event: tkinter.Event) -> bool:
        if flag := self.widget._texts[0].detect(event.x, event.y):
            self.widget.master._trigger_config.update(cursor="hand2")
            if self.widget.state == "normal":
                self.widget.update("hover")
                self.widget._texts[0].font.config(underline=True)
        else:
            if self.widget.state != "normal":
                self.widget.update("normal")
                self.widget._texts[0].font.config(underline=False)
        return flag

    def _click_left(self, _: tkinter.Event) -> bool:
        if flag := self.widget.state == "hover":
            self.widget.update("active")
        return flag

    def _release_left(self, event: tkinter.Event) -> bool:
        """"""
        if flag := self.widget._texts[0].detect(event.x, event.y):
            if self.widget.state == "active":
                self.widget.update("hover")
                self.widget._texts[0].font.config(underline=True)
                if self._command is not None:
                    self._command(*self._args)
        return flag


class Highlight(Button):
    """"""

    def _move_none(self, event: tkinter.Event) -> bool:
        if flag := self.widget._texts[0].detect(event.x, event.y):
            self.widget.master._trigger_config.update(cursor="hand2")
            if self.widget.state == "normal":
                self.widget.update("hover")
                animations.ScaleFontSize(
                    self.widget._texts[0], 150, delta=28).start()
        else:
            if self.widget.state != "normal":
                self.widget.update("normal")
                animations.ScaleFontSize(
                    self.widget._texts[0], 150, delta=24).start()
        return flag

    def _click_left(self, _: tkinter.Event) -> bool:
        if flag := self.widget.state == "hover":
            self.widget.update("active")
            animations.ScaleFontSize(
                self.widget._texts[0], 150, delta=26).start()
        return flag

    def _release_left(self, event: tkinter.Event) -> bool:
        """"""
        if flag := self.widget._texts[0].detect(event.x, event.y):
            if self.widget.state == "active":
                self.widget.update("hover")
                animations.ScaleFontSize(
                    self.widget._texts[0], 150, delta=28).start()
                if self._command is not None:
                    self._command(*self._args)
        return flag


class Switch(Button):
    """"""

    def _move_none(self, event: tkinter.Event) -> bool:
        if flag := self.widget._shapes[0].detect(event.x, event.y):
            self.widget.master._trigger_config.update(cursor="hand2")
            if self.widget.state.startswith("normal"):
                self.widget.update(
                    f"hover-{'on' if self.widget.get() else 'off'}")
        else:
            if not self.widget.state.startswith("normal"):
                self.widget.update(
                    f"normal-{'on' if self.widget.get() else 'off'}")
        return flag

    def _click_left(self, _: tkinter.Event) -> bool:
        if flag := self.widget.state.startswith("hover"):
            self.widget.update(
                f"active-{'on' if self.widget.get() else 'off'}", no_delay=True)
        return flag

    def _release_left(self, event: tkinter.Event) -> bool:
        """"""
        if flag := self.widget._shapes[0].detect(event.x, event.y):
            if self.widget.state.startswith("active"):
                boolean = not self.widget.get()
                self.widget.set(boolean)
                self.widget.update(
                    f"hover-{'on' if boolean else 'off'}", no_delay=True)
                if self._command is not None:
                    self._command(boolean)
        return flag


class CheckButton(Button):
    """"""

    def _click_left(self, _: tkinter.Event) -> bool:
        if flag := self.widget.state == "hover":
            self.widget.update("active", no_delay=True)
        return flag

    def _release_left(self, event: tkinter.Event) -> bool:
        """"""
        if flag := self.widget._shapes[0].detect(event.x, event.y):
            if self.widget.state == "active":
                self.widget.set(boolean := not self.widget.get())
                self.widget.update("hover", no_delay=True)
                if self._command is not None:
                    self._command(boolean)
        return flag


class RadioButton(CheckButton):
    """"""


class ProgressBar(Label):
    """"""


class Entry(Button):
    """"""

    def _move_none(self, event: tkinter.Event) -> bool:
        if flag := self.widget._shapes[0].detect(event.x, event.y):
            self.widget.master._trigger_config.update(cursor="xterm")
            if self.widget.state == "normal":
                self.widget.update("hover")
        else:
            if self.widget.state == "hover":
                self.widget.update("normal")
        return flag

    def _click_left(self, event: tkinter.Event) -> bool:
        if flag := self.widget._shapes[0].detect(event.x, event.y):
            self.widget.update("active")
            if self.widget.state == "active":  # Maybe widget is disabled
                self.widget.master._trigger_focus.update(
                    True, self.widget._texts[0].items[0])
                self.widget._texts[0].cursor_set(
                    self.widget._texts[0]._text_length())
        else:
            if self.widget.state != "normal":
                self.widget.update("normal")
        return flag

    def _release_left(self, event: tkinter.Event) -> bool:
        """"""
        return False

    def _input(self, event: tkinter.Event) -> bool:
        if self.widget.state == "active":
            match event.keysym:
                case "Right": self.widget._texts[0].move_area(1)
                case "Left": self.widget._texts[0].move_area(-1)
                case "BackSpace":
                    if self.widget._texts[0].value:
                        self.widget._texts[0].pop(1)
                case _:
                    if event.char.isprintable():
                        if not self.widget._texts[0].limitation():
                            self.widget._texts[0].append(event.char)
        return False
