"""All standard `Text` classes"""

from __future__ import annotations

__all__ = [
    "Information",
    "SingleLineText",
]

import bisect
import itertools
import math
import tkinter.font
import typing

import typing_extensions

from ..core import containers, virtual


class _CanvasTextProxy:

    def __init__(self, canvas: containers.Canvas, tag_or_id: str | int) -> None:
        self.canvas = canvas
        self.id = tag_or_id

    def _get_index(self, index: int) -> int:
        if index < 0:
            index += self.length()
        if 0 <= index <= self.length():
            return index
        raise IndexError("string index out of range")

    def length(self) -> int:
        """Length"""
        return self.canvas.index(self.id, "end")

    def get(self) -> str:
        """Get"""
        return self.canvas.itemcget(self.id, "text")

    def set(self, value: str, *, show: str | None = None) -> None:
        """Set"""
        if show:
            value = show * len(value)
        self.canvas.itemconfigure(self.id, text=value)

    def insert(self, index: int, value: str, *, show: str | None = None) -> None:
        """Insert"""
        if show:
            value = show * len(value)
        self.canvas.insert(self.id, self._get_index(index), value)

    def append(self, value: str, *, show: str | None = None) -> None:
        """Append"""
        self.insert(self.length(), value, show=show)

    def remove(self, start: int, end: int | None = None) -> None:
        """Remove"""
        start = self._get_index(start)
        end = start + 1 if end is None else self._get_index(end)
        self.canvas.dchars(self.id, start, end - 1)  # including

    def pop(self, index: int = -1) -> None:
        """Pop"""
        value = self.get()[index := self._get_index(index)]
        self.remove(index)
        return value

    def clear(self) -> None:
        """Clear"""
        self.canvas.itemconfigure(self.id, text="")

    def select_get(self) -> tuple[int, int] | None:
        """select get"""
        if self.canvas.select_item() != self.id:
            return None
        start = self.canvas.index(self.id, "sel.first")
        end = self.canvas.index(self.id, "sel.last")  # including
        return start, end + 1

    def select_set(self, start: int, end: int | None = None) -> None:
        """select set"""
        start = self._get_index(start)
        end = start + 1 if end is None else self._get_index(end)
        self.canvas.select_from(self.id, start)
        self.canvas.select_to(self.id, end - 1)  # including

    def select_all(self) -> None:
        """select all"""
        self.select_set(0, self.length())

    def select_clear(self) -> None:
        """select clear"""
        if self.select_get():
            self.canvas.select_clear()

    def cursor_get(self) -> int | None:
        """cursor get"""
        if self.canvas.focus() != self.id:
            return None
        return self.canvas.index(self.id, "insert")

    def cursor_set(self, index: int) -> None:
        """cursor set"""
        index = self._get_index(index)
        self.canvas.focus(self.id)
        self.canvas.icursor(self.id, index)

    def cursor_find(self, x: int) -> int:
        """cursor find"""
        x1, *_ = self.canvas.bbox(self.id)
        x -= x1 + 1
        font = tkinter.font.Font(font=self.canvas.itemcget(self.id, "font"))
        index = bisect.bisect_right(tuple(itertools.accumulate(self.get())), x, key=font.measure)

        distance_left = abs(x - font.measure(self.get()[:index]))
        distance_right = abs(x - font.measure(self.get()[:index+1]))

        if distance_right <= distance_left:
            index += 1

        return min(self.length(), index)


class Information(virtual.Text):
    """General information text"""

    @typing_extensions.override
    def display(self) -> None:
        """Display the `Element` on a `Canvas`"""
        self.items = [self.widget.master.create_text(
            0, 0, text=self.text, font=self.font, tags=("fill", "fill"), **self.kwargs)]

    @typing_extensions.override
    def coords(
        self,
        size: tuple[float, float] | None = None,
        position: tuple[float, float] | None = None,
    ) -> None:
        """Resize the `Element`"""
        super().coords(size, position)

        self.widget.master.coords(self.items[0], *self.center())

    def get(self) -> str:
        """Get the value of `Text`"""
        return self.text

    def set(self, text: str) -> None:
        """Set the value of `Text`"""
        if len(text) > self.limit >= 0:
            text = text[:self.limit]
        self.text = text
        self.widget.master.itemconfigure(self.items[0], text=self.text)

    def append(self, text: str) -> None:
        """Append value to the value of `Text`"""
        if len(self.text) + len(text) > self.limit >= 0:
            text = self.text[:self.limit-len(self.text)]
        self.text = self.text + text
        self.widget.master.itemconfigure(self.items[0], text=self.text)

    def delete(self, num: int) -> None:
        """Remove a portion of the `Text` value from the trail"""
        num = min(len(self.text), num)
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
        limit_width: int = 0,
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
        gradient_animation: bool = True,
        **kwargs,
    ) -> None:
        """
        * `widget`: parent widget
        * `relative_position`: position relative to its widgets
        * `size`: size of element
        * `text`: text value
        * `family`: font family
        * `fontsize`: font size
        * `weight`: weight of the font
        * `slant`: slant of the font
        * `underline`: wether text is underline
        * `overstrike`: wether text is overstrike
        * `align`: align mode of the text
        * `limit`: limit on the number of characters
        * `limit_width`: limit on the width of characters
        * `show`: display a value that obscures the original content
        * `placeholder`: a placeholder for the prompt
        * `name`: name of element
        * `gradient_animation`: Wether use animation to change color
        * `kwargs`: extra parameters for CanvasItem
        """
        self.left: int = 0
        self.right: int = 0
        self.anchor = "w" if align == "left" else "e" if align == "right" else "center"
        self.limit_width = limit_width
        virtual.Text.__init__(
            self, widget, relative_position, size, text=text, limit=limit, show=show,
            placeholder=placeholder, family=family, fontsize=fontsize, weight=weight, slant=slant,
            underline=underline, overstrike=overstrike, name=name,
            gradient_animation=gradient_animation, **kwargs)
        self.text_proxy = _CanvasTextProxy(widget.master, self.items[0])

    @typing_extensions.override
    def display(self) -> None:
        """Display the `Element` on a `Canvas`"""
        self.items = [
            self.widget.master.create_text(
                0, 0, text=self.text, font=self.font,
                anchor=self.anchor, tags=("fill", "fill"), **self.kwargs),
            self.widget.master.create_text(
                0, 0, text=self.placeholder, font=self.font,
                anchor=self.anchor, fill="#787878", **self.kwargs)]

    @typing_extensions.override
    def coords(
        self,
        size: tuple[float, float] | None = None,
        position: tuple[float, float] | None = None,
    ) -> None:
        """Resize the `Element`"""
        super().coords(size, position)

        x, y = self.center()
        if self.anchor == "w":
            x = self.position[0] + self._get_margin()
        elif self.anchor == "e":
            x = self.position[0] + self.size[0] - self._get_margin()

        self.widget.master.coords(self.items[0], x, y)
        self.widget.master.coords(self.items[1], x, y)

    def _get_margin(self) -> float:
        """Get the size of the spacing between the text and the border"""
        if self.items:
            _, y1, _, y2 = self.widget.master.bbox(self.items[0])
            return (self.size[1] - (y2-y1)) / 2
        return (self.size[1] - abs(self.font.cget("size"))) / 2

    def _is_overflow(self) -> bool:
        """Whether the text content extends beyond the text box"""
        x1, _, x2, _ = self.widget.master.bbox(self.items[0])
        width = (x2-x1) + self._get_margin()*2
        ratio = getattr(self.widget.master, "ratios", (1,))[0]
        if self.limit_width > 0:
            return width > self.limit_width*ratio
        return width >= self.size[0] + self.limit_width*ratio

    def _get_index(self, index: int) -> int:
        if index < 0:
            index += len(self.text)
        if 0 <= index <= len(self.text):
            return index
        raise IndexError("string index out of range")

    def get(self) -> str:
        """Get text of the element"""
        return self.text

    def set(self, value: str) -> bool:
        """Set text of the element"""
        self.clear()
        return self.append(value)

    def insert(self, index: int, value: str) -> bool:
        """Insert text to the location of the specified index"""
        if not self.text_proxy.length() and value:
            self.widget.master.itemconfigure(self.items[1], fill="")

        if flag := len(self.text + value) <= self.limit:
            index = self._get_index(index)
            key = self.left + index
            self.text = self.text[:key] + value + self.text[key:]
            self.text_proxy.insert(index, value, show=self.show)
            self.right += len(value)

            if index + len(value) == self.text_proxy.length():
                # Insert at the end
                while self._is_overflow():
                    self.text_proxy.remove(0)
                    self.left += 1
            else:
                while self._is_overflow():
                    self.text_proxy.remove(-1)
                    self.right -= 1

        return flag

    def append(self, value: str) -> bool:
        """Add some characters to the text cursor"""
        return self.insert(len(self.text), value)

    def remove(self, start: int, end: int | None = None) -> None:
        """Remove text within the specified index range"""
        if self.text_proxy.length() == 0:
            return None
        start = self._get_index(start)
        end = start + 1 if end is None else self._get_index(end)

        if start > end:
            start, end = end, start

        self.text = self.text[:self.left+start] + self.text[self.left+end:]
        self.text_proxy.remove(start, end)
        self.right -= end - start

        if self.right < len(self.text):  # There is a string on the right
            while not self._is_overflow():
                if self.right == len(self.text):
                    break
                self.text_proxy.append(self.text[self.right], show=self.show)
                self.right += 1
            else:
                self.text_proxy.remove(-1)
                self.right -= 1

        if self.left > 0:  # There is a string on the left
            while not self._is_overflow():
                if self.left == 0:
                    break
                self.left -= 1
                self.text_proxy.insert(0, self.text[self.left], show=self.show)
            else:
                self.text_proxy.remove(0)
                self.left += 1

        if not self.text_proxy.length():
            self.widget.master.itemconfigure(self.items[1], fill="#787878")

        return None

    def pop(self, index: int = -1) -> str:
        """Delete a character at the text cursor"""
        value = self.text[index]
        self.remove(index)
        return value

    def clear(self) -> None:
        """Clear"""
        self.text, self.left, self.right = "", 0, 0
        self.text_proxy.clear()

    def _move_left(self) -> None:
        """Move the text to the left as a whole, i.e. press the right arrow"""
        if self.right == len(self.text):
            return
        self.text_proxy.insert(
            length := self.text_proxy.length(), self.text[self.right], show=self.show)
        self.right += 1
        self.text_proxy.cursor_set(length+1)

        while self._is_overflow():
            self.text_proxy.remove(0)
            self.left += 1

    def _move_right(self) -> None:
        """Move the text to the right as a whole, i.e. press the left arrow"""
        if self.left == 0:
            return
        self.left -= 1
        self.text_proxy.insert(0, self.text[self.left], show=self.show)
        self.text_proxy.cursor_set(0)

        while self._is_overflow():
            self.text_proxy.remove(-1)
            self.right -= 1

    def cursor_move(self, count: int) -> None:
        """Move the index position of the text cursor"""
        index = self.text_proxy.cursor_get()
        if count < 0 < index:
            self.text_proxy.cursor_set(index + count)
        elif 0 < count and index < self.text_proxy.length():
            self.text_proxy.cursor_set(index + count)
        elif count < 0 and index == 0:
            self._move_right()
        elif count > 0 and index == self.text_proxy.length():
            self._move_left()

    def cursor_move_to(self, count: int) -> None:
        """Move the index position of the text cursor to a certain index"""
        return self.cursor_move(count - self.text_proxy.cursor_get())
