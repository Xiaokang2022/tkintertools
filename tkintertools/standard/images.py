"""All standard `Image` classes"""

from __future__ import annotations

__all__ = [
    "StillImage",
]

import typing_extensions

from ..core import virtual


class StillImage(virtual.Image):
    """A simple still image"""

    @typing_extensions.override
    def display(self) -> None:
        """Display the `Component` on a `Canvas`"""
        self.items = [self.widget.master.create_image(0, 0, image=self.image, **self.kwargs)]

    @typing_extensions.override
    def coords(
        self,
        size: tuple[float, float] | None = None,
        position: tuple[float, float] | None = None,
    ) -> None:
        """Resize the `Component`"""
        super().coords(size, position)

        self.widget.master.coords(self.items[0], *self.center())
