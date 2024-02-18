"""All standard Widgets"""
import typing

from . import core, features, images, shapes, texts


class Information(core.Widget):
    """"""

    def __init__(
        self,
        master: core.Canvas,
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        text: str = "",
        image: core.Image | None = None,
        through: bool = False,
    ) -> None:
        """"""
        core.Widget.__init__(
            self, master, position, size,
            shape=shapes.Rectangle(),
            feature=features.NoFeature(),
            text=texts.Information(text),
            image=image, through=through
        )


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
        image: core.Image | None = None,
        through: bool = False,
        radius: int = 5
    ) -> None:
        """"""
        core.Widget.__init__(
            self, master, position, size,
            shape=shapes.RoundedRectangle(
                radius=radius) if radius > 0 else shapes.Rectangle(),
            feature=features.Label(),
            text=texts.Information(text),
            image=image, through=through
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
        image: core.Image | None = None,
        through: bool = False,
        command: typing.Callable | None = None,
        radius: int = 5
    ) -> None:
        core.Widget.__init__(
            self, master, position, size,
            shape=shapes.RoundedRectangle(
                radius=radius) if radius > 0 else shapes.Rectangle(),
            feature=features.Button(command=command),
            text=texts.Information(text),
            image=image, through=through
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
        image: core.Image | None = None,
        through: bool = False,
        command: typing.Callable | None = None
    ) -> None:
        core.Widget.__init__(
            self, master, position, size,
            shape=shapes.NoShape(),
            feature=features.UnderLine(command=command),
            text=texts.Information(text),
            image=image, through=through
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
        image: core.Image | None = None,
        through: bool = False,
        command: typing.Callable | None = None
    ) -> None:
        core.Widget.__init__(
            self, master, position, size,
            shape=shapes.NoShape(),
            feature=features.Highlight(command=command),
            text=texts.Information(text),
            image=image, through=through
        )


__all__ = [
    "Information",
    "Label",
    "Button",
    "UnderlineButton",
    "HighlightButton",
]
