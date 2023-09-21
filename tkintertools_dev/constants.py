"""All constants"""

import enum

REQUIRE_PYTHON_VERSION = 3, 8, 0
PROCESS_DPI_AWARENESS = 1


class TKDefault:
    """"""
    DX = 11
    SIZE = 200, 200
    POSITION = None
    TITLE = 'tkt'
    ICONBITMAP = None
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


class TkState(enum.Enum):
    """"""

    NORMAL = 'normal'
    """"""

    ICON = 'icon'
    """"""

    ICONIC = 'iconic'
    """"""

    WITHDRAWN = 'withdrawn'
    """"""

    ZOOMED = 'zoomed'
    """"""


class BaseWidgetExpand(enum.Enum):
    """"""

    NONE = ''
    """"""

    X = 'x'
    """"""

    Y = 'y'
    """"""

    XY = 'xy'
    """"""


class BaseWidgetState(enum.Enum):
    """"""

    DEFAULT = 'default'
    """"""

    HOVER = 'hover'
    """"""

    SELECTED = 'selected'
    """"""

    DISABLED = 'disabled'
    """"""

    ERROR = 'error'
    """"""
