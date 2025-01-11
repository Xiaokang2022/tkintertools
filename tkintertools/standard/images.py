"""All standard `Image` classes"""

from __future__ import annotations

__all__ = [
    "StillImage",
    # "Smoke",
]

import typing_extensions

try:
    from PIL import Image
except ImportError:
    Image = None

from ..core import virtual
from ..toolbox import enhanced


class StillImage(virtual.Image):
    """A simple still image"""

    @typing_extensions.override
    def display(self) -> None:
        """Display the `Element` on a `Canvas`"""
        self.items = [self.widget.master.create_image(0, 0, image=self.image, **self.kwargs)]

    @typing_extensions.override
    def coords(
        self,
        size: tuple[float, float] | None = None,
        position: tuple[float, float] | None = None,
    ) -> None:
        """Resize the `Element`"""
        super().coords(size, position)

        self.widget.master.coords(self.items[0], *self.center())


class Smoke(virtual.Image):
    """A special Image with only one color"""

    def __init__(
        self,
        widget: virtual.Widget,
        relative_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        color: str | None = "#00000066",
        name: str | None = None,
        animation: bool = True,
        **kwargs,
    ) -> None:
        """
        * `widget`: parent widget
        * `relative_position`: position relative to its widgets
        * `size`: size of element
        * `color`: color of the image object of the element
        * `name`: name of element
        * `animation`: Wether use animation to change color
        * `kwargs`: extra parameters for CanvasItem
        """
        if Image is None:
            raise RuntimeError("Package 'pillow' is missing.")

        virtual.Image.__init__(self, widget, relative_position, size,
                               name=name, gradient_animation=animation, **kwargs)

        self.image = self.initail_image = enhanced.PhotoImage(
            Image.new("RGBA", (round(self.size[0]), round(self.size[1])), color))

    @typing_extensions.override
    def display(self) -> None:
        """Display the `Element` on a `Canvas`"""
        self.items = [self.widget.master.create_image(0, 0, image=self.image, **self.kwargs)]

    @typing_extensions.override
    def coords(
        self,
        size: tuple[float, float] | None = None,
        position: tuple[float, float] | None = None,
    ) -> None:
        """Resize the `Element`"""
        super().coords(size, position)

        self.widget.master.coords(self.items[0], *self.center())
