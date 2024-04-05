"""Support some extra Widgets"""

import pathlib
import typing

from .. import constants, core, theme
from ..stdandard import features, images, shapes, texts


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
        styles: dict[typing.Literal["Shape", "Text"],
                     dict[core.State, core.Style]] | None = None,
    ) -> None:
        """"""
        core.Widget.__init__(
            self, master, position, size,
            text=texts.Information(text=text, family=family, size=fontsize, weight=weight,
                                   slant=slant, underline=underline, overstrike=overstrike),
            shape=shapes.RoundedRectangle(),
            image=images.NoImage(),
            feature=features.NoFeature(),
            styles=styles if styles else theme.get(
                self, pathlib.Path(__file__).parent)
        )


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
        styles: dict[typing.Literal["Shape", "Text"],
                     dict[core.State, core.Style]] | None = None,
    ) -> None:
        core.Widget.__init__(
            self, master, position, size,
            text=texts.Information(text=text, family=family, size=fontsize, weight=weight,
                                   slant=slant, underline=underline, overstrike=overstrike),
            shape=shapes.NoShape(),
            image=images.NoImage(),
            feature=features.UnderLine(command=command),
            styles=styles if styles else theme.get(
                self, pathlib.Path(__file__).parent)
        )


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
        styles: dict[typing.Literal["Shape", "Text"],
                     dict[core.State, core.Style]] | None = None,
    ) -> None:
        core.Widget.__init__(
            self, master, position, size,
            text=texts.Information(text=text, family=family, size=fontsize, weight=weight,
                                   slant=slant, underline=underline, overstrike=overstrike),
            shape=shapes.NoShape(),
            image=images.NoImage(),
            feature=features.Highlight(command=command),
            styles=styles if styles else theme.get(
                self, pathlib.Path(__file__).parent)
        )


__all__ = [
    "Information",
    "UnderlineButton",
    "HighlightButton",
]
