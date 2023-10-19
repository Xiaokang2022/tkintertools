"""All constants"""

import enum
import tkinter

REQUIRE_PYTHON_VERSION = 3, 8, 0
PROCESS_SYSTEM_DPI_AWARE = 1


class TKDefault:
    """"""

    SIZE = 200, 200
    POSITION = None, None
    TITLE = None
    ICONBITMAP = None
    STATE = None
    ALPHA = 1
    FULLSCREEN = False
    TOOLWINDOW = False
    TOPMOST = False
    TRANSPARENTCOLOR = None
    KEEP_RATIO = False
    MAXSIZE = None, None
    MINSIZE = None, None
    RESIZABLE = True, True
    OVERRIDEREDIRECT = False
    SHUTDOWN = None


class TkState(enum.Enum):  # FIXME: not fully support for Linux
    """"""

    NORMAL = "normal"
    """"""

    ICON = "icon"
    """"""

    ICONIC = "iconic"
    """"""

    WITHDRAWN = "withdrawn"
    """"""

    ZOOMED = "zoomed"
    """"""


class BaseWidgetExpand(enum.Enum):
    """"""

    NONE = ""
    """"""

    X = "x"
    """"""

    Y = "y"
    """"""

    XY = "xy"
    """"""


class BaseWidgetState(enum.Enum):
    """"""

    DEFAULT = "default"
    """"""

    HOVER = "hover"
    """"""

    SELECTED = "selected"
    """"""

    DISABLED = "disabled"
    """"""

    ERROR = "error"
    """"""
