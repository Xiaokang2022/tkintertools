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
