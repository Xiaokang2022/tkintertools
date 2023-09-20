"""all constants"""

import enum

# class Tk
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


# class BaseWidget
class Expand(enum.Enum):
    """The expand mode of the widget."""
    NONE = ''
    X = 'x'
    Y = 'y'
    XY = 'xy'


class State(enum.Enum):
    """The state of the widget."""
    DEFAULT = 'default'
    HOVER = 'hover'
    SELECTED = 'selected'
    DISABLED = 'disabled'
    ERROR = 'error'
