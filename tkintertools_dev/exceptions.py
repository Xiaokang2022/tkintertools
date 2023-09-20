"""all exceptions"""

import typing


class StateError(ValueError):
    """"""

    def __init__(self, value: typing.Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"Parameter state_ must be 'default', 'hover', 'selected', 'disabled' or 'error', not {self.value}"


class SystemError(RuntimeError):
    """"""

    def __init__(self, system: typing.Literal['Windows', 'Linux', 'Macos']) -> None:
        self.system = system

    def __str__(self) -> str:
        return f"This class is only available under the Windows system, not {self.system}"
