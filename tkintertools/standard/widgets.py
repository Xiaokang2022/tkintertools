"""All standard Widgets"""

import math
import typing

from .. import constants, core
from ..animate import animations, controllers
from . import features, images, shapes, texts


class Label(core.Widget):
    """
    Label widget

    Used to display information
    """

    def __init__(
        self,
        master: core.Canvas,
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        text: str = "",
        family: str = constants.FONT,
        fontsize: int = constants.SIZE,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
    ) -> None:
        """"""
        core.Widget.__init__(self, master, position, size)
        if constants.IS_WIN10:
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self)
        texts.Information(self, text=text, family=family, size=fontsize, weight=weight,
                          slant=slant, underline=underline, overstrike=overstrike)
        features.Label(self)


class Button(core.Widget):
    """
    Button Widget
    """

    def __init__(
        self,
        master: core.Canvas,
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        text: str = "",
        family: str = constants.FONT,
        fontsize: int = constants.SIZE,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        command: typing.Callable | None = None,
    ) -> None:
        core.Widget.__init__(self, master, position, size)
        if constants.IS_WIN10:
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self)
        texts.Information(self, text=text, family=family, size=fontsize, weight=weight,
                          slant=slant, underline=underline, overstrike=overstrike)
        features.Button(self, command=command)


class Switch(core.Widget):
    """"""

    def __init__(
        self,
        master: core.Canvas,
        position: tuple[int, int],
        length: int,
        *,
        default: bool = False,
        command: typing.Callable[[bool], typing.Any] | None = None,
    ) -> None:
        core.Widget.__init__(self, master, position, (length, length / 2),
                             state=f"normal-{"on" if default else "off"}",
                             animation=False)
        shapes.SemicircularRectangle(self)
        shapes.Oval(self, rel_position=(length/12, length/12),
                    size=(length/3, length/3))
        features.Switch(self, command=command)
        if default:
            self.set(default)

    def get(self) -> bool:
        """"""
        return self.state.endswith("on")

    def set(self, value: bool) -> None:
        """"""
        self.update(f"{self.state.split("-")[0]}-{"on" if value else "off"}")
        dx = self.shapes[0].w/2 if value else -self.shapes[0].w/2
        animations.MoveComponent(
            self.shapes[1], 250, controllers.smooth, delta=(dx, 0), fps=60).start()


class CheckButton(core.Widget):
    """"""

    def __init__(
        self,
        master: core.Canvas,
        position: tuple[int, int],
        length: int,
        *,
        default: bool = False,
        command: typing.Callable[[bool], typing.Any] | None = None,
    ) -> None:
        core.Widget.__init__(self, master, position, (length, length))
        if constants.IS_WIN10:
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self)
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


class RadioButton(core.Widget):
    """"""

    def __init__(
        self,
        master: core.Canvas,
        position: tuple[int, int],
        length: int,
        *,
        command: typing.Callable[[int], typing.Any] | None = None,
    ) -> None:
        core.Widget.__init__(self, master, position, (length, length))
        shapes.Oval(self, name="Oval_1")
        shapes.Oval(self, name="Oval_2", rel_position=(
            self.w/4, self.h/4), size=(self.w/2, self.h/2))
        features.RadioButton(self, command=command)

    def get(self) -> bool:
        """"""
        return self.shapes[1].visible

    def set(self, value: bool) -> None:
        """"""
        if value:
            return self.shapes[1].appear()
        self.shapes[1].disappear()


class ProgressBar(core.Widget):
    """"""

    def __init__(
        self,
        master: core.Canvas,
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        command: typing.Callable[[], typing.Any] | None = None,
    ) -> None:
        self.value: float = 0
        core.Widget.__init__(self, master, position, size)
        if constants.IS_WIN10:
            shapes.Rectangle(self, name="Rectangle_1")
            shapes.Rectangle(self, name="Rectangle_2", size=(
                0, self.h*0.8), rel_position=(self.h*0.1, self.h*0.1))
        else:
            shapes.SemicircularRectangle(self, name="SemicircularRectangle_1")
            shapes.SemicircularRectangle(
                self, name="SemicircularRectangle_2", size=(self.h*0.7, self.h*0.7), rel_position=(self.h*0.15, self.h*0.15))
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


class Entry(core.Widget):
    """"""

    def __init__(
        self,
        master: core.Canvas,
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        limit: int = math.inf
    ) -> None:
        core.Widget.__init__(self, master, position, size)
        if constants.IS_WIN10:
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self)
        texts.SingleLineText(self, text="", limit=limit)
        features.Entry(self)

    def get(self) -> str:
        """"""
        return self.value

    def set(self, value: str) -> None:
        """"""
        self.value = value

    def append(self, value: str) -> None:
        """"""
        self.value += value

    def delete(self, count: int) -> None:
        """"""
        self.value = self.value[:-count]

    def clear(self) -> None:
        """"""
        self.value = ""


class Information(core.Widget):
    """"""

    def __init__(
        self,
        master: core.Canvas,
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        text: str = "",
        family: str = constants.FONT,
        fontsize: int = constants.SIZE,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
    ) -> None:
        """"""
        core.Widget.__init__(self, master, position, size)
        if constants.IS_WIN10:
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self)
        texts.Information(self, text=text, family=family, size=fontsize, weight=weight,
                          slant=slant, underline=underline, overstrike=overstrike)


class UnderlineButton(core.Widget):
    """"""

    def __init__(
        self,
        master: core.Canvas,
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        text: str = "",
        family: str = constants.FONT,
        fontsize: int = constants.SIZE,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        command: typing.Callable | None = None,
    ) -> None:
        core.Widget.__init__(self, master, position, size)
        texts.Information(self, text=text, family=family, size=fontsize, weight=weight,
                          slant=slant, underline=underline, overstrike=overstrike)
        features.UnderLine(self, command=command)


class HighlightButton(core.Widget):
    """"""

    def __init__(
        self,
        master: core.Canvas,
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        text: str = "",
        family: str = constants.FONT,
        fontsize: int = constants.SIZE,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        command: typing.Callable | None = None,
    ) -> None:
        core.Widget.__init__(self, master, position, size)
        texts.Information(self, text=text, family=family, size=fontsize, weight=weight,
                          slant=slant, underline=underline, overstrike=overstrike)
        features.Highlight(self, command=command)


# class Slider(core.Widget):
#     """"""

#     def __init__(
#         self,
#         master: core.Canvas,
#         position: tuple[int, int],
#         length: int,
#         *,
#         default: float = 0,
#         command: typing.Callable[[float], typing.Any] | None = None,
#     ) -> None:
#         self.value = default
#         core.Widget.__init__(self, master, position, (length, 8))
#         if constants.IS_WIN10:
#             shapes.Rectangle(self)
#             shapes.Rectangle(self, size=(self.h, self.h*3),
#                              rel_position=(100, -self.h))
#         else:
#             shapes.SemicircularRectangle(self)
#             shapes.Oval(self, size=(self.h*3, self.h*3),
#                         rel_position=(100, -self.h))
#         features.Slider(self, command=command)

#     def get(self) -> bool:
#         """"""
#         return self.value

#     def set(self, value: float) -> None:
#         """"""
#         self.value = 0 if value < 0 else 1 if value > 1 else value
