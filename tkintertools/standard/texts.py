"""All standard Texts"""

import math
import typing

from ..core import virtual

__all__ = [
    "Information",
    "SingleLineText",
]


class Information(virtual.Text):
    """General information text"""

    # @typing.override
    def display(self) -> None:
        self.items.append(self.widget.master.create_text(
            *self.center(), text=self.text, font=self.font, justify=self.justify,
            anchor=self.anchor, tags=("fill", "fill")))

    def get(self) -> str:
        """Get the value of `Text`"""
        return self.text

    def set(self, text: str) -> None:
        """Set the value of `Text`"""
        if len(text) > self.limit:
            text = text[:self.limit]
        self.text = text
        self.widget.master.itemconfigure(self.items[0], text=self.text)

    def append(self, text: str) -> None:
        """Append value to the value of `Text`"""
        if len(self.text) + len(text) > self.limit:
            text = self.text[:self.limit-len(self.text)]
        self.text = self.text + text
        self.widget.master.itemconfigure(self.items[0], text=self.text)

    def delete(self, num: int) -> None:
        """Remove a portion of the `Text` value from the trail"""
        if num > len(self.text):
            num = len(self.text)
        self.text = self.text[:-num]
        self.widget.master.itemconfigure(self.items[0], text=self.text)

    def clear(self) -> None:
        """Clear the value of `Text`"""
        self.text = ""
        self.widget.master.itemconfigure(self.items[0], text=self.text)


class SingleLineText(virtual.Text):
    """Single-line editable text"""

    def __init__(
        self,
        widget: virtual.Widget,
        relative_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        text: str = "",
        limit: int = math.inf,
        show: str | None = None,
        placeholder: str = "",
        align: typing.Literal["left", "center", "right"] = "left",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal["normal", "bold"] = "normal",
        slant: typing.Literal["roman", "italic"] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        name: str | None = None,
        animation: bool = True,
        styles: dict[str, dict[str, str]] | None = None,
        **kwargs,
    ) -> None:
        """
        * `widget`: parent widget
        * `relative_position`: position relative to its widgets
        * `size`: size of component
        * `text`: text value
        * `family`: font family
        * `fontsize`: font size
        * `weight`: weight of the font
        * `slant`: slant of the font
        * `underline`: wether text is underline
        * `overstrike`: wether text is overstrike
        * `align`: align mode of the text
        * `limit`: limit on the number of characters
        * `show`: display a value that obscures the original content
        * `placeholder`: a placeholder for the prompt
        * `name`: name of component
        * `animation`: Wether use animation to change color
        * `styles`: style dict of component
        * `kwargs`: extra parameters for CanvasItem
        """
        self.left: int = 0
        self.right: int = 0
        anchor = "w" if align == "left" else "e" if align == "right" else "center"
        virtual.Text.__init__(self, widget, relative_position, size,
                              text=text, limit=limit, show=show, placeholder=placeholder,
                              anchor=anchor, family=family, fontsize=fontsize, weight=weight,
                              slant=slant, underline=underline, overstrike=overstrike,
                              name=name, styles=styles, animation=animation, **kwargs)

    # @typing.override
    def display(self) -> None:
        x, y = self.center()
        if self.anchor == "w":
            x = self.position[0] + self.get_gap()
        elif self.anchor == "e":
            x = self.position[0] + self.size[0] - self.get_gap()
        self.items.append(
            self.widget.master.create_text(
                x, y, text=self.text, font=self.font, justify=self.justify,
                anchor=self.anchor, tags=("fill", "fill"))),
        self.items.append(
            self.widget.master.create_text(
                x, y, text=self.placeholder, font=self.font, justify=self.justify,
                anchor=self.anchor, fill="#787878"))

    def _text_get(self) -> str:
        """Get the actual text that appears on the component"""
        return self.widget.master.itemcget(self.items[0], "text")

    def _text_set(self, value: str) -> None:
        """Set the actual text that appears on the component"""
        if self.show:
            value = self.show * len(value)
        self.widget.master.itemconfigure(self.items[0], text=value)

    def _text_insert(self, index: int, value: str) -> None:
        """Insert the actual text that appears on the component"""
        if self.show:
            value = self.show * len(value)
        self.widget.master.insert(self.items[0], index, value)

    def _text_delete(self, start: int, end: int | typing.Literal["end"]) -> None:
        """Delete the actual text that appears on the component"""
        self.widget.master.dchars(self.items[0], start, end)

    def get(self) -> str:
        """Get text of the component"""
        return self.text

    def set(self, value: str) -> None:
        """Set text of the component"""
        self.text = value  # BUG
        self._text_set(value)

    def insert(self, index: int, value: str) -> None:
        """"""
        if index < 0:
            index = self._text_length() + index
        key_index = self.left+index
        self.text = self.text[:key_index] + value + self.text[key_index:]
        self._text_insert(index, value)

        while self._text_overflow():
            length = self._text_length()
            if self.cursor_get() == length:
                self._text_delete(0, 0)
            else:
                self._text_delete(length-1, "end")

    def get_gap(self) -> float:
        """"""  # BUG
        return (self.size[1]-abs(self.font["size"])) / 3

    def delete(self, start: int, end: int | typing.Literal["end"]) -> None:
        """[start, end]"""
        if end == "end":
            self.text = self.text[:self.left+start]
        else:
            self.text = self.text[:self.left+start] + \
                self.text[self.left+end+1:]
        self._text_delete(start, end)

        while self.overflow():
            if self.cursor_get() == 0:
                break

    def select_set(self, start: int, end: int) -> None:
        """[start, end]"""
        self.widget.master.select_from(self.items[0], start)
        self.widget.master.select_to(self.items[0], end)

    def select_get(self) -> tuple[int, int]:
        """"""
        start = self.widget.master.index(self.items[0], "sel.first")
        end = self.widget.master.index(self.items[0], "sel.last")
        return start, end

    def select_all(self) -> None:
        """"""
        self.select_set(0, self._text_length())

    def select_clear(self) -> None:
        """"""
        self.widget.master.select_clear()

    def _text_length(self) -> int:
        """Get the length of actual text that appears on the component"""
        return self.widget.master.index(self.items[0], "end")

    def width(self) -> int:
        """Get the width of actual text that appears on the component"""
        x1, y1, x2, y2 = self.widget.master.bbox(self.items[0])
        return x2 - x1

    def cursor_set(self, index: int) -> int:
        """"""
        if index < 0:
            index = self._text_length() + index + 1
        self.widget.master.icursor(self.items[0], index)

    def cursor_get(self) -> int:
        """"""
        return self.widget.master.index(self.items[0], "insert")

    def limitation(self) -> int:
        """"""
        if (count := len(self.text) - self.limit) > 0:
            return count
        return 0

    def _text_overflow(self) -> bool:
        """"""
        return self.font.measure(self._text_get()) + self.get_gap()*2 >= self.size[0] - 2

    def overflow(self) -> bool:
        """"""
        return self.font.measure(self.text) >= self.size[0] - 2

    def update_add(self, anchor_left: bool) -> None:
        """"""
        if anchor_left:
            while self._text_overflow():
                self._text_set(self._text_get()[:-1])
        else:
            while self._text_overflow():
                self._text_set(self._text_get()[1:])

    def move_cursor(self, count: int) -> None:
        """"""
        index = self.cursor_get()
        if count < 0 < index:
            return self.cursor_set(index + count)
        elif 0 < count and index < self._text_length():
            return self.cursor_set(index + count)
        elif count < 0 and index == 0:
            print(1)
        elif count > 0 and index == self._text_length():
            if self._text_overflow():
                print(2)

    def pop(self, count: int) -> None:
        """"""
        if (index := self.cursor_get() - 1) >= 0:
            self.delete(index, index)

    def append(self, value: str) -> None:
        """"""
        if self._text_length() < self.limit:
            self.insert(self.cursor_get(), value)
            self.right += len(value)
