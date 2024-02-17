"""All standard Widgets"""
import typing

from . import core, features, images, shapes, texts


class Label(core.Widget):
    """
    Label widget

    Used to display information
    """

    def __init__(
        self,
        master: core.Canvas,
        size: tuple[int, int],
        position: tuple[int, int],
        *,
        text: str = "",
        image: core.Image | None = None,
        through: bool = False
    ) -> None:
        """"""
        core.Widget.__init__(
            self, master, size, position,
            shape=shapes.Rectangle(),
            feature=features.NoFeature(),
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
        size: tuple[int, int],
        position: tuple[int, int],
        *,
        text: str = "",
        image: core.Image | None = None,
        through: bool = False,
        command: typing.Callable | None = None
    ) -> None:
        core.Widget.__init__(
            self, master, size, position,
            shape=shapes.Rectangle(),
            feature=features.Button(command=command),
            text=texts.Information(text),
            image=image, through=through
        )


class UnderLineButton(core.Widget):
    """"""

    def __init__(
        self,
        master: core.Canvas,
        size: tuple[int, int],
        position: tuple[int, int],
        *,
        text: str = "",
        image: core.Image | None = None,
        through: bool = False,
        command: typing.Callable | None = None
    ) -> None:
        core.Widget.__init__(
            self, master, size, position,
            shape=shapes.NoShape(),
            feature=features.UnderLine(command=command),
            text=texts.Information(text),
            image=image, through=through
        )
