"""Some auxiliary classes"""

import math
import typing

from ..core import constants, containers, virtual
from ..toolbox import enhanced, tools
from . import features, images, shapes, texts

__all__ = [
    "_AuxiliaryButton",
    "_AuxiliaryLabel",
]


class _AuxiliaryLabel(virtual.Widget):
    """"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] | None = None,
        *,
        text: str = "",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: typing.Literal["left", "center", "right"] = "left",
        anchor: typing.Literal["n", "e", "w", "s", "nw",
                               "ne", "sw", "se", "center"] = "center",
        image: enhanced.PhotoImage | None = None,
        ignore: typing.Literal["left", "right"] = "left",
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        if size is None:
            size = tools.get_text_size(text, family, fontsize, padding=10)
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.HalfRoundedRectangle(self, ignore=ignore)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self, text=text, family=family, fontsize=fontsize,
                          weight=weight, slant=slant, underline=underline,
                          overstrike=overstrike, justify=justify, anchor=anchor)
        features.LabelFeature(self)


class _AuxiliaryButton(virtual.Widget):
    """"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] | None = None,
        *,
        text: str = "",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: typing.Literal["left", "center", "right"] = "left",
        anchor: typing.Literal["n", "e", "w", "s", "nw",
                               "ne", "sw", "se", "center"] = "center",
        command: typing.Callable | None = None,
        image: enhanced.PhotoImage | None = None,
        ignore: typing.Literal["left", "right"] = "left",
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        if size is None:
            size = tools.get_text_size(text, family, fontsize, padding=10)
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.HalfRoundedRectangle(self, ignore=ignore)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self, text=text, family=family, fontsize=fontsize,
                          weight=weight, slant=slant, underline=underline,
                          overstrike=overstrike, justify=justify, anchor=anchor)
        features.ButtonFeature(self, command=command)


class _AuxiliaryInputBox(virtual.Widget):
    """"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] | None = None,
        *,
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        align: typing.Literal["left", "right", "center"] = "left",
        placeholder: str = "",
        show: str | None = None,
        limit: int = math.inf,
        image: enhanced.PhotoImage | None = None,
        ignore: typing.Literal["left", "right"] = "left",
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        if size is None:
            size = 200, tools.get_text_size(
                "", family, fontsize, padding=10)[1]
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.HalfRoundedRectangle(self, name=".out", ignore=ignore)
            shapes.HalfRoundedRectangle(
                self, name=".in", size=(self.size[0], self.size[1]-3), ignore=ignore)
        if image is not None:
            images.StillImage(self, image=image)
        texts.SingleLineText(self, family=family, fontsize=fontsize, weight=weight,
                             slant=slant, underline=underline, overstrike=overstrike,
                             align=align, limit=limit, show=show, placeholder=placeholder)
        features.InputBoxFeature(self)

    def get(self) -> str:
        """Get the value of the Entry"""
        return self._texts[0].get()

    def set(self, value: str) -> None:
        """Set the text value of the Entry"""
        self._texts[0].set(value)

    def append(self, value: str) -> None:
        """Append text to Entry"""
        self._texts[0].append(value)

    def delete(self, count: int) -> None:
        """Delete a specified amount of text"""
        self._texts[0].pop(count)

    def clear(self) -> None:
        """Clear the text value of the Entry"""
        self.set("")
