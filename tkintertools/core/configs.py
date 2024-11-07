"""All configs of tkintertools"""

import math
import platform
import tkinter
import types
import typing
import warnings

import typing_extensions

from ..theme import dark, light

try:
    import darkdetect
except ImportError:
    darkdetect = None

__all__ = [
    "Env",
    "Font",
    "Theme",
    "Constant",
    "reset_configs",
]


class Env:
    """Configurations of environment."""

    system: str
    is_dark: bool

    default_root: tkinter.Tk | None

    @classmethod
    def reset(cls) -> None:
        """Reset all configs."""
        cls.system = cls.get_default_system()
        cls.is_dark = bool(darkdetect.isDark()) if darkdetect else False

    @staticmethod
    def get_default_system() -> str:
        """Get the system of environment."""
        if (system := platform.system()) == "Windows":
            # If Python version is 3.10, the function below gets an error result
            # SYSTEM = f"Windows{platform.win32_ver()[0]}"
            if int(platform.win32_ver()[1].split(".")[-1]) >= 22000:
                return "Windows11"
            return "Windows10"
        return system

    @typing_extensions.override
    # @classmethod  # XXX: Using this decorator will produce an error, strangely
    def __getattr__(self, name: str) -> typing.Any:
        if name == "default_root":
            return tkinter._default_root
        return super().__getattr__(name)  # pylint: disable=no-member


Env = Env()  # Camouflaged as a class to solve the strange problem above


class Font:
    """Configurations of font."""

    family: str
    size: int

    @classmethod
    def reset(cls) -> None:
        """Reset all configs."""
        cls.family = cls.get_default_family()
        cls.size = -20

    @staticmethod
    def get_default_family() -> str:
        """Get font family."""
        if (system := Env.get_default_system()).startswith("Windows"):
            return "Microsoft YaHei"
        if system == "Darwin":
            return "PingFang SC"
        return "Noto Sans"


class Theme:
    """Configurations of theme."""

    light: types.ModuleType | dict
    dark: types.ModuleType | dict
    color_mode: typing.Literal["light", "dark", "system"]
    """
    The color mode of the current program, `"system"` is the following system,
    `"light"` is the light color, and `"dark"` is the dark color
    """

    @classmethod
    def reset(cls) -> None:
        """Reset all configs."""
        cls.light, cls.dark = cls.get_default_themes()
        cls.color_mode = "system"

    @staticmethod
    def get_default_themes() -> tuple[types.ModuleType, types.ModuleType]:
        """Get default themes."""
        return light, dark


class Constant:
    """Configurations of font."""

    __sys_call_flag: bool = False

    GOLDEN_RATIO: float

    @classmethod
    def reset(cls) -> None:
        """Reset all configs."""
        cls.__sys_call_flag = True
        cls.GOLDEN_RATIO = (math.sqrt(5)-1) / 2
        cls.__sys_call_flag = False

    @typing_extensions.override
    @classmethod
    def __setattr__(cls, name, value: typing.Any) -> None:
        if not cls.__sys_call_flag:
            warnings.warn("", UserWarning, 2)
        return super().__setattr__(name, value)


def reset_configs() -> None:
    """Reset all configs."""
    Env.reset()
    Font.reset()
    Theme.reset()
    Constant.reset()


reset_configs()
