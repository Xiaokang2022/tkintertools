"""All standard Widgets"""

import typing

from .. import constants, core
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
                             state=f"normal-{"on" if default else "off"}")
        shapes.SemicircularRectangle(self)
        shapes.Oval(self, delta=(-length/4, 0, 1/3, 2/3))
        features.Switch(self, command=command)
        if default:
            self.set(default)

    def get(self) -> bool:
        """"""
        return self.state.endswith("on")

    def set(self, value: bool) -> None:
        """"""
        self.update(f"{self.state.split("-")[0]}-{"on" if value else "off"}")
        dx = self.shapes[0].width/2 if value else -self.shapes[0].width/2
        self.shapes[1].move(dx, 0)


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
        texts.Information(self)
        features.CheckButton(self, command=command)
        if default:
            self.set(default)

    def get(self) -> bool:
        """"""
        return bool(self.texts[0].get())

    def set(self, value: bool) -> None:
        """"""
        if value:
            return self.texts[0].set("    ✔️")
        self.texts[0].clear()


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
        shapes.Oval(self, name="Oval_2", delta=(0, 0, 0.5, 0.5))
        features.RadioButton(self, command=command)

    def get(self) -> bool:
        """"""

    def set(self, value: int) -> None:
        """"""


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
        core.Widget.__init__(self, master, position, size)
        if constants.IS_WIN10:
            shapes.Rectangle(self, name="Rectangle_1")
            shapes.Rectangle(self, name="Rectangle_2", delta=(0, 0, 0.5, 0.8))
        else:
            shapes.SemicircularRectangle(self, name="SemicircularRectangle_1")
            shapes.SemicircularRectangle(
                self, name="SemicircularRectangle_2", delta=(0, 0, 0.5, 0.8))
        features.ProgressBar(self)

    def get(self) -> bool:
        """"""

    def set(self, value: float) -> None:
        """"""


# class Slider(core.Widget):
#     """"""

#     def __init__(
#         self,
#         master: core.Canvas,
#         position: tuple[int, int],
#         length: int,
#         *,
#         command: typing.Callable[[float], typing.Any] | None = None,
#     ) -> None:
#         core.Widget.__init__(self, master, position, (length, 10))
#         if constants.IS_WIN10:
#             shapes.Rectangle(self)
#             shapes.Rectangle(self, delta=(0, 0, 0.02, 3))
#         else:
#             shapes.SemicircularRectangle(self)
#             shapes.Oval(self, delta=(0, 0, 0.05, 2))
#         features.Slider(self, command=command)

#     def get(self) -> bool:
#         """"""

#     def set(self, value: float) -> None:
#         """"""


# class Dial(core.Widget):
#     """"""

#     def __init__(
#         self,
#         master: core.Canvas,
#         position: tuple[int, int],
#         length: int,
#         *,
#         command: typing.Callable[[float], typing.Any] | None = None,
#     ) -> None:
#         core.Widget.__init__(self, master, position, (length, length))
#         shapes.Oval(self)
#         shapes.Oval(
#             self, delta=(-self.position[0]*0.35, 0, 0.2, 0.2))
#         features.Dial(self, command=command)

#     def get(self) -> bool:
#         """"""

#     def set(self, value: float) -> None:
#         """"""
