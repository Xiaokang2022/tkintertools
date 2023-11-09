"""All exceptions"""

import typing

from .constants import *


class EnvironmentError(RuntimeError):
    """"""

    def __init__(self, version):
        # type: (tuple) -> None
        self.version = "Python%d.%d.%d" % version[:3]

    def __str__(self):
        # type: () -> str
        require_version = "Python%d.%d.%d" % REQUIRE_PYTHON_VERSION
        return f"Your Python version is too low({self.version}), it's require {require_version}"


class SystemError(RuntimeError):
    """"""

    def __init__(self, system):
        # type: (typing.Literal['Windows', 'Linux', 'Macos']) -> None
        self.system = system

    def __str__(self):
        # type: () -> str
        return f"This class is only available under the Windows system, not {self.system}"


class StateError(ValueError):
    """"""

    def __init__(self, value):
        # type: (typing.Any) -> None
        self.value = value

    def __str__(self):
        # type: () -> str
        return f"Parameter state_ must be 'default', 'hover', 'selected', 'disabled' or 'error', not {self.value}"
