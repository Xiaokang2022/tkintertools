"""All standard Widgets"""

import math
import typing

from ..animation import animations, controllers
from ..core import constants, containers, virtual
from ..toolbox import enhanced
from . import features, images, shapes, texts

__all__ = [
    "Information",
    "Label",
    "Button",
    "Switch",
    "Entry",
    "CheckButton",
    "RadioButton",
    "ProgressBar",
    "UnderlineButton",
    "HighlightButton",
]


class Information(virtual.Widget):
    """"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] = (0, 0),
        *,
        text: str = "",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """"""
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self, text=text, family=family, size=fontsize, weight=weight,
                          slant=slant, underline=underline, overstrike=overstrike)


class Label(virtual.Widget):
    """
    Label widget

    Used to display information
    """

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] = (120, 50),
        *,
        text: str = "",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """"""
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self, text=text, family=family, size=fontsize, weight=weight,
                          slant=slant, underline=underline, overstrike=overstrike)
        features.Label(self)


class Button(virtual.Widget):
    """
    Button Widget
    """

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] = (120, 50),
        *,
        text: str = "",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        command: typing.Callable | None = None,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self, text=text, family=family, size=fontsize, weight=weight,
                          slant=slant, underline=underline, overstrike=overstrike)
        features.Button(self, command=command)


class Switch(virtual.Widget):
    """"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        length: int = 60,
        *,
        default: bool = False,
        command: typing.Callable[[bool], typing.Any] | None = None,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        virtual.Widget.__init__(self, master, position, (length, length / 2),
                                state=f"normal-{'on' if default else 'off'}",
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self, name=".out")
            shapes.Rectangle(self, name=".in", rel_position=(
                length/12, length/12), size=(length/3, length/3), animation=False)
        else:
            shapes.SemicircularRectangle(self)
            shapes.Oval(self, rel_position=(length/12, length/12),
                        size=(length/3, length/3), animation=False)
        if image is not None:
            images.StillImage(self, image=image)
        features.Switch(self, command=command)
        if default:
            self.set(default)

    def get(self) -> bool:
        """"""
        return self.state.endswith("on")

    def set(self, value: bool) -> None:
        """"""
        self.update(
            f"{self.state.split('-')[0]}-{'on' if value else 'off'}", no_delay=True)
        dx = self.shapes[0].w/2 if value else -self.shapes[0].w/2
        animations.MoveComponent(
            self.shapes[1], 250, (dx, 0), controller=controllers.smooth, fps=60).start()


class Entry(virtual.Widget):
    """"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] = (250, 50),
        *,
        limit: int = math.inf,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self, name=".out")
            shapes.RoundedRectangle(self, name=".in", size=(self.w, self.h-3))
        if image is not None:
            images.StillImage(self, image=image)
        texts.SingleLineText(self, text="", limit=limit)
        features.Entry(self)

    def get(self) -> str:
        """"""
        return self.texts[0].get()

    def set(self, value: str) -> None:
        """"""
        self.texts[0].set(value)

    def append(self, value: str) -> None:
        """"""
        self.texts[0].append(value)

    def delete(self, count: int) -> None:
        """"""
        self.texts[0].pop(count)

    def clear(self) -> None:
        """"""
        self.set("")


class CheckButton(virtual.Widget):
    """"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        length: int = 30,
        *,
        default: bool = False,
        command: typing.Callable[[bool], typing.Any] | None = None,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        virtual.Widget.__init__(self, master, position, (length, length),
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self).set("✔")
        features.CheckButton(self, command=command)
        self.set(default)

    def get(self) -> bool:
        """"""
        return self.texts[0].visible

    def set(self, value: bool) -> None:
        """"""
        if value:
            return self.texts[0].appear()
        self.texts[0].disappear()


class RadioButton(virtual.Widget):
    """"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        length: int = 24,
        *,
        default: bool = False,
        command: typing.Callable[[int], typing.Any] | None = None,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        virtual.Widget.__init__(self, master, position, (length, length),
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self, name=".out")
            shapes.Rectangle(self, name=".in", rel_position=(
                self.w/4, self.h/4), size=(self.w/2, self.h/2)).disappear()
        else:
            shapes.Oval(self, name=".out")
            shapes.Oval(self, name=".in", rel_position=(
                self.w/4, self.h/4), size=(self.w/2, self.h/2)).disappear()
        if image is not None:
            images.StillImage(self, image=image)
        features.RadioButton(self, command=command)
        if default:
            self.shapes[1].appear()

    def get(self) -> bool:
        """"""
        return self.shapes[1].visible

    def set(self, value: bool) -> None:
        """"""
        if value:
            return self.shapes[1].appear()
        self.shapes[1].disappear()


class ProgressBar(virtual.Widget):
    """"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] = (400, 20),
        *,
        command: typing.Callable[[], typing.Any] | None = None,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        self.value: float = 0
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self, name=".out")
            shapes.Rectangle(self, name=".in", size=(
                0, self.h*0.8), rel_position=(self.h*0.1, self.h*0.1))
        else:
            shapes.SemicircularRectangle(self, name=".out")
            shapes.SemicircularRectangle(self, name=".in", size=(
                self.h*0.7, self.h*0.7), rel_position=(self.h*0.15, self.h*0.15))
        if image is not None:
            images.StillImage(self, image=image)
        features.ProgressBar(self)
        self.shapes[1].disappear()
        self.command = command

    def get(self) -> float:
        """"""
        return self.value

    def set(self, value: float) -> None:
        """"""
        self.value = 0 if value < 0 else 1 if value > 1 else value
        if self.value == 0:
            return self.shapes[1].disappear()
        elif not self.shapes[1].visible:
            self.shapes[1].appear()
        if isinstance(self.shapes[1], shapes.Rectangle):
            x, y = self.shapes[1].x, self.shapes[1].y
            w, h = (self.w - self.h*0.2)*self.value, self.shapes[1].h
            self.master.coords(self.shapes[1].items[0], x, y, x+w, y+h)
        else:
            w, h = self.w - self.h*0.3 - self.shapes[1].h, self.shapes[1].h
            x, y = self.shapes[1].x + h/2, self.shapes[1].y
            w *= self.value
            self.master.coords(self.shapes[1].items[2], x, y, x+w, y+h)
            self.master.coords(self.shapes[1].items[5], x, y, x+w, y)
            self.master.coords(self.shapes[1].items[6], x, y+h, x+w, y+h)
            self.master.coords(
                self.shapes[1].items[1], x+w-h/2, y, x+w+h/2, y+h)
            self.master.coords(
                self.shapes[1].items[4], x+w-h/2, y, x+w+h/2, y+h)
        if value == 1 and self.command is not None:
            self.command()


class UnderlineButton(virtual.Widget):
    """"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] = (0, 0),
        *,
        text: str = "",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        command: typing.Callable | None = None,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = False,
    ) -> None:
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self, text=text, family=family, size=fontsize, weight=weight,
                          slant=slant, underline=underline, overstrike=overstrike)
        features.Underline(self, command=command)


class HighlightButton(virtual.Widget):
    """"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] = (0, 0),
        *,
        text: str = "",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        command: typing.Callable | None = None,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self, text=text, family=family, size=fontsize, weight=weight,
                          slant=slant, underline=underline, overstrike=overstrike)
        features.Highlight(self, command=command)
