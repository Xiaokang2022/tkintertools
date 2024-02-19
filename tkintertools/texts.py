"""All standard Texts"""

from . import core


class NoText(core.Text):
    """"""


class Information(core.Text):
    """"""

    def display(self, master: core.Canvas, position: tuple[int, int]) -> None:
        core.Text.display(self, master, position)
        self._items.append(master.create_text(
            *position, text=self._text, font=self._font,
            angle=self._angle, anchor=self._anchor))


__all__ = [
    "NoText",
    "Information",
]
