"""Enhanced versions of some tkinter classes and functions"""

import functools
import tkinter

try:
    import PIL.ImageTk as ImageTk
except ImportError:
    ImageTk = None

__all__ = [
    "PhotoImage",
]


class PhotoImage(tkinter.PhotoImage):
    """Enhanced version of `tkinter.PhotoImage`"""

    @functools.cached_property
    def _data(self) -> list[list[str]]:
        """Returns image data in the form of a string."""
        # self.tk.call(self, "data", "-format", "png -alpha 0")
        # XXX: Add alpha channel
        return [line.split() for line in self.tk.call(self, "data")]

    @functools.cached_property
    def _transparency_data(self) -> list[list[bool]]:
        """Returns image transparency data."""
        return [[self.transparency_get(x, y) for x in range(self.width())] for y in range(self.height())]

    def scale(self, x: float, y: float) -> "PhotoImage":
        """Scale the PhotoImage"""
        width = round(x*self.width())
        height = round(y*self.height())
        new_image = PhotoImage(width=width, height=height)
        new_image.put([[self._data[int(y_/y)][int(x_/x)]
                      for x_ in range(width)] for y_ in range(height)])
        for x_ in range(width):
            for y_ in range(height):
                if self._transparency_data[int(y_/y)][int(x_/x)]:
                    new_image.transparency_set(x_, y_, True)
        return new_image


if ImageTk is not None:

    class PhotoImage(ImageTk.PhotoImage, tkinter.PhotoImage):
        """Pillow version of `tkinter.PhotoImage`"""

        def scale(self, x: float, y: float) -> "PhotoImage":
            """Scale the PhotoImage"""
            width = round(x*self.width())
            height = round(y*self.height())
            return PhotoImage(ImageTk.getimage(self).resize((width, height)))
