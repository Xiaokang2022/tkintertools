"""All standard Features"""

import tkinter
import typing

from ..animation import animations, controllers
from ..core import virtual
from ..standard import shapes

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
    "Slider",
]


class Label(virtual.Feature):
    """Feature of Label"""

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
    """Feature of Button"""

    def __init__(
        self,
        widget: virtual.Widget,
        *,
        command: typing.Callable | None = None,
        args: tuple = (),
    ) -> None:
        """
        * `widget`: parent widget
        * `command`: callback function
        * `args`: arguments of callback function
        """
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
    """Feature of underline"""

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
    """Feature of highlight"""

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
    """Feature of Switch"""

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
    """Feature of CheckButton"""

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
    """Feature of RadioButton"""


class ProgressBar(Label):
    """Feature of ProgressBar"""


class Entry(Button):
    """Feature of Entry"""

    def __init__(
        self,
        widget: virtual.Widget,
        *,
        command: typing.Callable[..., typing.Any] | None = None,
        args: tuple = (),
    ) -> None:
        super().__init__(widget, command=command, args=args)
        self._start_index: int | None = None
        self._end_index: int | None = None

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
                self._start_index = self.widget._texts[0].cursor_find(event.x)
                self.widget._texts[0].cursor_set(self._start_index)
                self.widget.master.itemconfigure(
                    self.widget._texts[0].items[1], fill="")
        else:
            if self.widget.state != "normal":
                self.widget.update("normal")
                if not self.widget._texts[0].get():
                    self.widget.master.itemconfigure(
                        self.widget._texts[0].items[1], fill="#787878")
        self.widget._texts[0].select_clear()
        return flag

    def _move_left(self, event: tkinter.Event) -> bool:
        if self.widget.state == "active":
            self.widget.master._trigger_config.update(cursor="xterm")
            self._end_index = self.widget._texts[0].cursor_find(event.x)
            self.widget._texts[0].cursor_set(self._end_index)
            if self._start_index < self._end_index:
                self.widget._texts[0].select_set(
                    self._start_index, self._end_index-1)
            elif self._start_index > self._end_index:
                self.widget._texts[0].select_set(
                    self._end_index, self._start_index-1)
            else:
                self.widget._texts[0].select_clear()
            return True
        return False

    def _release_left(self, event: tkinter.Event) -> bool:
        return False

    def _input(self, event: tkinter.Event) -> bool:
        if self.widget.state == "active":
            select = self.widget._texts[0].select_get()
            match event.keysym:
                case "Right":
                    if select is None:
                        self.widget._texts[0].cursor_move(1)
                    else:
                        self.widget._texts[0].select_clear()
                        self.widget._texts[0].cursor_move_to(select[1]+1)
                case "Left":
                    if select is None:
                        self.widget._texts[0].cursor_move(-1)
                    else:
                        self.widget._texts[0].select_clear()
                        self.widget._texts[0].cursor_move_to(select[0])
                case "BackSpace":
                    if select is not None:
                        self.widget._texts[0].select_clear()
                        self.widget._texts[0].delete(*select)
                    elif self.widget._texts[0].text:
                        self.widget._texts[0].pop()
                case _:
                    if len(event.char) and event.char.isprintable():
                        if select is not None:
                            self.widget._texts[0].select_clear()
                            self.widget._texts[0].delete(*select)
                        self.widget._texts[0].append(event.char)
                        return None
        return False

    def _copy(self, event: tkinter.Event) -> bool:
        if flag := self.widget.state == "active":
            if (select := self.widget._texts[0].select_get()) is not None:
                self.widget.master.clipboard_clear()
                self.widget.master.clipboard_append(
                    self.widget._texts[0]._text_get()[select[0]: select[1]+1])
        return flag

    def _paste(self, event: tkinter.Event) -> bool:
        if flag := self.widget.state == "active":
            if (select := self.widget._texts[0].select_get()) is not None:
                self.widget._texts[0].select_clear()
                self.widget._texts[0].delete(*select)
            if value := self.widget.master.clipboard_get():
                self.widget._texts[0].append(value)
        return flag

    def _cut(self, event: tkinter.Event) -> bool:
        if flag := self._copy(event):
            self.widget._texts[0].delete(*self.widget._texts[0].select_get())
            self.widget._texts[0].select_clear()
        return flag


class Slider(virtual.Feature):
    """Feature of Slider"""

    def __init__(self, widget: virtual.Widget) -> None:
        super().__init__(widget)
        self._temp_position: tuple[float, float] | None = None

    def _move_none(self, event: tkinter.Event) -> bool:
        if flag := self.widget._shapes[2].detect(event.x, event.y):
            if self.widget.state == "normal":
                self.widget.update("hover")
                if isinstance(self.widget._shapes[-1], shapes.Oval):
                    self.widget._shapes[-1].coords((self.widget.size[1]*2/3, self.widget.size[1]*2/3), (
                        self.widget._shapes[-2].position[0]+self.widget.size[1]/6, self.widget._shapes[-2].position[1]+self.widget.size[1]/6))
        else:
            if self.widget.state == "hover":
                self.widget.update("normal")
                if isinstance(self.widget._shapes[-1], shapes.Oval):
                    self.widget._shapes[-1].coords((self.widget.size[1]/2, self.widget.size[1]/2), (
                        self.widget._shapes[-2].position[0]+self.widget.size[1]/4, self.widget._shapes[-2].position[1]+self.widget.size[1]/4))
        return flag

    def _click_left(self, event: tkinter.Event) -> bool:
        if self.widget.state == "hover":
            self._temp_position = event.x, event.y
            self.widget.update("active")
        elif self.widget.state != "disabled" and self.widget._shapes[0].detect(event.x, event.y):
            self._temp_position = event.x, event.y
            self.widget.update("active")
            temp_value = self.widget.value
            if isinstance(self.widget._shapes[-1], shapes.Oval):
                self.widget._shapes[-1].coords((self.widget.size[1]*2/3, self.widget.size[1]*2/3), (
                    self.widget._shapes[-2].position[0]+self.widget.size[1]/6, self.widget._shapes[-2].position[1]+self.widget.size[1]/6))
                next_value = (event.x-self.widget.position[0]-self.widget.size[1]/2) / (
                    self.widget.size[0]-self.widget.size[1])
            else:
                next_value = (event.x-self.widget.position[0]-self.widget.size[1]/5) / (
                    self.widget.size[0]-self.widget.size[1]*2/5)
            delta = next_value - temp_value
            animations.Animation(150, controllers.smooth,
                                 callback=lambda k: self.widget.set(temp_value + delta*k), fps=60).start()

    def _move_left(self, event: tkinter.Event) -> bool:
        if self._temp_position is not None:
            if isinstance(self.widget._shapes[-1], shapes.Oval):
                delta = (
                    event.x-self._temp_position[0]) / (self.widget.size[0]-self.widget.size[1])
            else:
                delta = (
                    event.x-self._temp_position[0]) / (self.widget.size[0]-self.widget.size[1]*2/5)
            self._temp_position = event.x, event.y
            self.widget.set(self.widget.value + delta)

    def _release_left(self, event: tkinter.Event) -> bool:
        if self.widget.state == "active":
            self._temp_position = None
            self.widget.update("hover")
