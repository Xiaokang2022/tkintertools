"""All standard Widgets"""

import typing

from .. import constants, core, theme
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
        styles: dict[typing.Literal["Shape", "Text"],
                     dict[core.State, core.Style]] | None = None,
    ) -> None:
        """"""
        core.Widget.__init__(
            self, master, position, size,
            text=texts.Information(text=text, family=family, size=fontsize, weight=weight,
                                   slant=slant, underline=underline, overstrike=overstrike),
            shape=shapes.Rectangle() if constants.IS_WIN10 else shapes.RoundedRectangle(),
            image=images.NoImage(),
            feature=features.Label(),
            styles=styles if styles else theme.get(self)
        )


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
        styles: dict[typing.Literal["Shape", "Text"],
                     dict[core.State, core.Style]] | None = None,
    ) -> None:
        core.Widget.__init__(
            self, master, position, size,
            text=texts.Information(text=text, family=family, size=fontsize, weight=weight,
                                   slant=slant, underline=underline, overstrike=overstrike),
            shape=shapes.Rectangle() if constants.IS_WIN10 else shapes.RoundedRectangle(),
            image=images.NoImage(),
            feature=features.Button(command=command),
            styles=styles if styles else theme.get(self)
        )


__all__ = [
    "Label",
    "Button",
]
