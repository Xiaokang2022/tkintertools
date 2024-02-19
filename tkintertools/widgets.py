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
        shape: core.Shape | None = None,
        text: str = "",
        image: core.Image | None = None,
        through: bool = False,
    ) -> None:
        """"""
        core.Widget.__init__(
            self, master, position, size,
            shape=shapes.Rectangle() if shape is None else shape,
            text=texts.Information(text),
            image=None,
            feature=features.NoFeature(),
            through=through,
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
        shape: core.Shape | None = None,
        text: str = "",
        image: core.Image | None = None,
        through: bool = False,
        radius: int = 5
    ) -> None:
        """"""
        if shape is None:
            (shape := shapes.RoundedRectangle(radius=radius) if radius > 0 else shapes.Rectangle()).set_style(
                normal=("#E1E1E1", "#C0C0C0"),
                hover=("#E5F1FB", "#288CDB")
            )
        core.Widget.__init__(
            self, master, position, size,
            shape=shape,
            text=texts.Information(text),
            image=None,
            feature=features.Label(),
            through=through
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
        shape: core.Shape | None = None,
        text: str = "",
        image: core.Image | None = None,
        through: bool = False,
        command: typing.Callable | None = None,
        radius: int = 5
    ) -> None:
        if shape is None:
            (shape := shapes.RoundedRectangle(radius=radius)if radius > 0 else shapes.Rectangle()).set_style(
                normal=("#E1E1E1", "#C0C0C0"),
                hover=("#E5F1FB", "#288CDB"),
                click=("#CCE4F7", "#4884B4"))
        core.Widget.__init__(
            self, master, position, size,
            shape=shape,
            text=texts.Information(text),
            image=None,
            feature=features.Button(command=command),
            through=through
        )


class UnderlineButton(core.Widget):
    """"""

    def __init__(
        self,
        master: core.Canvas,
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        shape: core.Shape | None = None,
        text: str = "",
        image: core.Image | None = None,
        through: bool = False,
        command: typing.Callable | None = None
    ) -> None:
        (text := texts.Information(text)).set_style(
            hover="blue", click="purple")
        core.Widget.__init__(
            self, master, position, size,
            shape=shapes.NoShape() if shape is None else shape,
            text=text,
            image=None,
            feature=features.UnderLine(command=command),
            through=through
        )


class HighlightButton(core.Widget):
    """"""

    def __init__(
        self,
        master: core.Canvas,
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        shape: core.Shape | None = None,
        text: str = "",
        image: core.Image | None = None,
        through: bool = False,
        command: typing.Callable | None = None
    ) -> None:
        (text := texts.Information(text)).set_style(normal="grey")
        core.Widget.__init__(
            self, master, position, size,
            shape=shapes.NoShape() if shape is None else shape,
            text=text,
            image=None,
            feature=features.Highlight(command=command),
            through=through
        )


__all__ = [
    "Information",
    "Label",
    "Button",
    "UnderlineButton",
    "HighlightButton",
]
