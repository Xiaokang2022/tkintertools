"""All standard Features"""

import tkinter
import typing

from . import core


class NoFeature(core.Feature):
    """"""

    def __init__(self) -> None:
        """"""
        self._events: list[str] = []

    def _event_process(self, event: tkinter.Event) -> bool:
        """"""
        return False
