"""All standard Images"""

from ..core import virtual

__all__ = [
    "StillImage",
]


class StillImage(virtual.Image):
    """A simple still image"""

    # @typing.override
    def display(self) -> None:
        self.items = [self.widget.master.create_image(0, 0, image=self.image)]

    # @typing.override
    def coords(self, size: tuple[float, float] | None = None, position: tuple[float, float] | None = None) -> None:
        super().coords(size, position)

        self.widget.master.coords(self.items[0], *self.center())
