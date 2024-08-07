"""All constants"""

import math
import platform

FONT: str = None
SIZE: int = None
SYSTEM: str = None
GOLDEN_RATIO: float = (math.sqrt(5)-1) / 2

__all__ = [
    "FONT",
    "SIZE",
    "SYSTEM",
    "reset",
]


def reset() -> None:
    """Reset all constants to default value"""
    global FONT, SIZE, SYSTEM
    SIZE = -20
    if (SYSTEM := platform.system()) == "Windows":
        # When the Python version is 3.10, the function below gets an error result
        # SYSTEM = f"Windows{platform.win32_ver()[0]}"
        if int(platform.win32_ver()[1].split(".")[-1]) >= 22000:
            SYSTEM = "Windows11"
        else:
            SYSTEM = "Windows10"
    FONT = "Microsoft YaHei" if SYSTEM.startswith(
        "Windows") else "PingFang SC" if SYSTEM == "Darwin" else "Noto Sans"


reset()
