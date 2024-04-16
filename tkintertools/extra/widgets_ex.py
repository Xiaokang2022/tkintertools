"""Support some extra Widgets"""

import pathlib
import typing

from .. import constants, core, style
from ..stdandard import features, images, shapes, texts

THEME_PATH = pathlib.Path(__file__).parent / "theme"


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
        shapes.RoundedRectangle(
            self, styles=style.get(self, "RoundedRectangle", path=THEME_PATH))
        texts.Information(self, text=text, family=family, size=fontsize, weight=weight,
                          slant=slant, underline=underline, overstrike=overstrike,
                          styles=style.get(self, "Information", path=THEME_PATH))


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
                          slant=slant, underline=underline, overstrike=overstrike,
                          styles=style.get(self, "Information", path=THEME_PATH))
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
                          slant=slant, underline=underline, overstrike=overstrike,
                          styles=style.get(self, "Information", path=THEME_PATH))
        features.Highlight(self, command=command)
