"""All global configuration options.

Some options are read-only, but most of them can be changed, and once changed,
they will take effect globally for the program. Some changes take effect
immediately, but some need to take effect when the relevant option is invoked.
"""

from __future__ import annotations

__all__ = [
    "Env",
    "Font",
    "Constant",
    "reset",
]

import ctypes
import math
import platform
import tkinter
import typing


class _DefaultRootDescriptor:
    """A simple descriptor for `tkinter._default_root`."""

    def __get__(self, *args, **kwargs) -> tkinter.Tk:
        """Returns the current default root.

        In some cases, the method also returns `tkinter.Tk` and `None`, but
        this can happen if the usage is not recommended.
        """
        return tkinter._get_default_root()


class Env:
    """Configurations for default environment values."""

    # Global configurations
    system: str
    theme: typing.Literal["light", "dark"]

    # Default parameters for widgets
    gradient_animation: bool
    auto_update: bool

    # Dynamic value
    root = _DefaultRootDescriptor()

    @classmethod
    def reset(cls) -> None:
        """Reset all configuration options."""
        cls.system = cls.get_default_system()
        cls.theme = "light"
        cls.gradient_animation = True
        cls.auto_update = True

    @staticmethod
    def get_default_system() -> str:
        """Get the system of environment."""
        if platform.system() == "Windows":
            # If Python version is 3.10, the function below gets an error result
            # SYSTEM = f"Windows{platform.win32_ver()[0]}"
            if int(platform.win32_ver()[1].split(".")[-1]) >= 22000:
                return "Windows11"
            return "Windows10"
        return platform.system()


class Font:
    """Configurations for default font."""

    family: str
    size: int

    @classmethod
    def reset(cls) -> None:
        """Reset all configuration options."""
        cls.family = cls.get_default_family()
        cls.size = -20

    @staticmethod
    def get_default_family() -> str:
        """Get the default font family."""
        match platform.system():
            case "Windows": return "Microsoft YaHei"
            case "Darwin": return "SF Pro"
            case _: return "Noto Sans"


class Constant:
    """All Constants."""

    GOLDEN_RATIO: typing.Final[float] = (math.sqrt(5)-1) / 2
    """The golden ratio, which is needed to automatically calculate the color
    of widget on `"disabled"` state. It is READ-ONLY."""

    PREDEFINED_EVENTS: typing.Final[tuple[str, ...]] = (
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
    """Predefined events that can be used directly without registration. It is
    READ-ONLY."""

    PREDEFINED_VIRTUAL_EVENTS: typing.Final[tuple[str, ...]] = (
        "<<Copy>>",
        "<<Paste>>",
        "<<Cut>>",
        "<<SelectAll>>",
        "<<Redo>>",
        "<<Undo>>",
    )
    """Predefined virtual events that can be used directly without
    registration. It is READ-ONLY."""


def reset() -> None:
    """Reset all configuration options."""
    Env.reset()
    Font.reset()


reset()

if Env.system.startswith("Windows"):
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Set Windows DPI awareness
