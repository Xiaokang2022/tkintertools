"""All configs of tkintertools"""

from __future__ import annotations

import collections.abc
import math
import platform
import tkinter
import types
import typing

from ..theme import dark, light

try:
    import darkdetect
except ImportError:
    pass

__all__ = [
    "Env",
    "Font",
    "Theme",
    "Constant",
    "reset_configs",
]


class _DefaultRootDescriptor:
    """A simple descriptor about tkinter._default_root."""

    def __get__(self, obj: typing.Any, cls: typing.Any) -> tkinter.Tk:
        """Return the current default root."""
        return tkinter._get_default_root()


class Env:
    """Configurations of environment."""

    system: str
    is_dark: bool
    default_callback: collections.abc.Callable[[tkinter.Event], typing.Literal[False]]

    enable_animation: bool

    default_root = _DefaultRootDescriptor()

    @classmethod
    def reset(cls) -> None:
        """Reset all configs."""
        cls.system = cls.get_default_system()
        cls.is_dark = bool(darkdetect.isDark()) if globals().get("darkdetect") else False
        cls.enable_animation = True
        cls.default_callback = lambda _: False

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
    """All Constants"""

    GOLDEN_RATIO: typing.Final[float] = (math.sqrt(5)-1) / 2

    PRE_DEFINED_EVENTS: typing.Final[tuple[str, ...]] = (
        "<KeyPress>",
        "<KeyRelease>",
        "<Button-1>",
        "<Button-2>",
        "<Button-3>",
        "<Button-4>",
        "<Button-5>",
        "<ButtonRelease-1>",
        "<ButtonRelease-2>",
        "<ButtonRelease-3>",
        "<MouseWheel>",
        "<Motion>",
        "<B1-Motion>",
        "<B2-Motion>",
        "<B3-Motion>",
        "<Configure>",
    )

    PRE_DEFINED_VIRTUAL_EVENTS: typing.Final[tuple[str, ...]] = (
        "<<Copy>>",
        "<<Paste>>",
        "<<Cut>>",
        "<<SelectAll>>",
        "<<Redo>>",
        "<<Undo>>",
    )


def reset_configs() -> None:
    """Reset all configs."""
    Env.reset()
    Font.reset()
    Theme.reset()


reset_configs()
