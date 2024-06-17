"""All standard Texts"""

import typing

from ..core import virtual

__all__ = [
    "Information",
    "SingleLineText",
]


class Information(virtual.Text):
    """"""

    # @typing.override
    def display(self) -> None:
        self.items.append(self.widget.master.create_text(
            *self.center(), text=self.value, font=self.font, justify=self.justify,
            anchor=self.anchor, tags=("fill", "fill")))

    def get(self) -> str:
        """Get the value of `Text`"""
        return self.value

    def set(self, text: str) -> None:
        """Set the value of `Text`"""
        if len(text) > self.limit:
            text = text[:self.limit]
        self.value = text
        self.widget.master.itemconfigure(self.items[0], text=self.value)

    def append(self, text: str) -> None:
        """Append value to the value of `Text`"""
        if len(self.value) + len(text) > self.limit:
            text = self.value[:self.limit-len(self.value)]
        self.value = self.value + text
        self.widget.master.itemconfigure(self.items[0], text=self.value)

    def delete(self, num: int) -> None:
        """Remove a portion of the `Text` value from the trail"""
        if num > len(self.value):
            num = len(self.value)
        self.value = self.value[:-num]
        self.widget.master.itemconfigure(self.items[0], text=self.value)

    def clear(self) -> None:
        """Clear the value of `Text`"""
        self.value = ""
        self.widget.master.itemconfigure(self.items[0], text=self.value)


class SingleLineText(virtual.Text):
    """"""

    # @typing.override
    def display(self) -> None:
        self.items.append(self.widget.master.create_text(
            *self.center(), text=self.value, font=self.font, justify=self.justify,
            anchor=self.anchor, tags=("fill", "fill")))

    def _text_get(self) -> str:
        """"""
        return self.widget.master.itemcget(self.items[0], "text")

    def _text_set(self, value: str) -> None:
        """"""
        self.widget.master.itemconfigure(self.items[0], text=value)

    def _text_insert(self, index: int, value: str) -> None:
        """"""
        self.widget.master.insert(self.items[0], index, value)

    def _text_delete(self, start: int, end: int | typing.Literal["end"]) -> None:
        """"""
        self.widget.master.dchars(self.items[0], start, end)

    def get(self) -> str:
        """"""
        return self.value

    def set(self, value: str) -> None:
        """"""
        self.value = value
        self._text_set(value)

    def insert(self, index: int, value: str) -> None:
        """"""
        if index < 0:
            index = self._text_length() + index
        key_index = self.left+index
        self.value = self.value[:key_index] + value + self.value[key_index:]
        self._text_insert(index, value)

        while self._text_overflow():
            length = self._text_length()
            if self.cursor_get() == length:
                self._text_delete(0, 0)
            else:
                self._text_delete(length-1, "end")

    def delete(self, start: int, end: int | typing.Literal["end"]) -> None:
        """[start, end]"""
        if end == "end":
            self.value = self.value[:self.left+start]
        else:
            self.value = self.value[:self.left+start] + \
                self.value[self.left+end+1:]
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
        """"""
        return self.widget.master.index(self.items[0], "end")

    def bbox(self) -> tuple[int, int, int, int]:
        """"""
        return self.widget.master.bbox(self.items[0])

    def width(self) -> int:
        """"""
        x1, y1, x2, y2 = self.bbox()
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
        if (count := len(self.value) - self.limit) > 0:
            return count
        return 0

    def get_face_text(self, add: bool) -> str:
        """"""
        if add:
            for i in range(-2, 3):
                if self.font.measure(self.value[self.left: self.right+i]) >= self.size[0]:
                    self.right += i
                    break
        else:
            for i in range(-2, 3):
                if self.font.measure(self.value[self.left-i: self.right+i]) >= self.size[0]:
                    self.left += i
                    break
        return self.value[self.left: self.right]

    def _text_overflow(self) -> bool:
        """"""
        return self.font.measure(self._text_get()) >= self.size[0] - 2

    def overflow(self) -> bool:
        """"""
        return self.font.measure(self.value) >= self.size[0] - 2

    def update_add(self, anchor_left: bool) -> None:
        """"""
        if anchor_left:
            while self._text_overflow():
                self._text_set(self._text_get()[:-1])
        else:
            while self._text_overflow():
                self._text_set(self._text_get()[1:])

    def move_area(self, count: int) -> None:
        """"""
        index = self.cursor_get()
        if count < 0 < index:
            return self.cursor_set(index + count)
        if 0 < count and index < self._text_length():
            return self.cursor_set(index + count)

    def pop(self, count: int) -> None:
        """"""
        if (index := self.cursor_get() - 1) >= 0:
            self.delete(index, index)

    def append(self, value: str) -> None:
        """"""
        if self._text_length() < self.limit:
            self.insert(self.cursor_get(), value)
