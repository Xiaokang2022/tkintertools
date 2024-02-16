"""All standard Widgets"""

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
        shape: core.Shape | None = None,
        feature: core.Feature | None = None,
        text: core.Text | str = "",
        image: core.Image | None = None,
        through: bool = False
    ) -> None:
        """"""
        core.Widget.__init__(
            self, master, size, position,
            shape=shapes.Rectangle() if shape is None else shape,
            feature=features.NoFeature() if feature is None else feature,
            text=texts.NormalText(text) if isinstance(text, str) else text,
            image=image, through=through
        )
