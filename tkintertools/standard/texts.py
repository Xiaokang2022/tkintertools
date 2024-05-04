"""All standard Texts"""

from .. import core


class NoText(core.Text):
    """"""

    def display(self) -> None:
        pass


class Information(core.Text):
    """"""

    def display(self) -> None:
        self.items.append(self.widget.master.create_text(
            *self.center(), text=self.value, font=self.font, tags="text"))


class SingleLineText(core.Text):
    """"""

    def display(self) -> None:
        self.items.append(self.widget.master.create_text(
            *self.center(), text=self.value, font=self.font, tags="text"))

    def get(self) -> str:
        """"""
        return self.widget.master.itemcget(self.items[0], "text")

    def set(self, value: str) -> None:
        """"""
        self.widget.master.itemconfigure(self.items[0], text=value)

    def append(self, value: str) -> None:
        """"""
        self.insert(-1, value)

    def insert(self, index: int, value: str) -> None:
        """"""
        if index < 0:
            index = self.length() + index
        self.widget.master.insert(self.items[0], index, value)

    def delete(self, start: int, end: int) -> None:
        """[start, end]"""
        self.widget.master.dchars(self.items[0], start, end)

    def pop(self, count: int) -> None:
        """"""
        self.widget.master.dchars(self.items[0], self.length()-count, "end")

    def clear(self) -> None:
        """"""
        self.set("")

    def set_selection(self, start: int, end: int) -> None:
        """[start, end]"""
        self.widget.master.select_from(self.items[0], start)
        self.widget.master.select_to(self.items[0], end)

    def get_selection(self) -> tuple[int, int]:
        """"""
        start = self.widget.master.index(self.items[0], "sel.first")
        end = self.widget.master.index(self.items[0], "sel.last")
        return start, end

    def select_all(self) -> None:
        """"""
        self.set_selection(0, self.length())

    def select_clear(self) -> None:
        """"""
        self.widget.master.select_clear()

    def length(self) -> int:
        """"""
        return self.widget.master.index(self.items[0], "end")

    def bbox(self) -> tuple[int, int, int, int]:
        """"""
        return self.widget.master.bbox(self.items[0])

    def width(self) -> int:
        """"""
        x1, y1, x2, y2 = self.bbox()
        return x2 - x1

    def set_cursor(self, index: int) -> int:
        """"""
        if index < 0:
            index = self.length() + index + 1
        self.widget.master.icursor(self.items[0], index)

    def get_cursor(self) -> int:
        """"""
        return self.widget.master.index(self.items[0], "insert")


class MultipleLineText(core.Text):
    """"""
