"""All constants"""

import platform  # Get information about the platform

# System constants

SYSTEM = platform.system()
"""Operating System"""

PROCESS_SYSTEM_DPI_AWARE = 1
"""Default DPI aware"""

# Color constants

COLOR_FILL_BUTTON = "#E1E1E1", "#E5F1FB", "#CCE4F7", "#E0E0E0"
"""Default `Button` fill color"""

COLOR_OUTLINE_BUTTON = "#C0C0C0", "#288CDB", "#4884B4", "#D0D0D0"
"""Default `Button` outline color"""

COLOR_FILL_LABEL = COLOR_FILL_BUTTON
"""Default `Label` fill color"""

COLOR_OUTLINE_LABEL = COLOR_OUTLINE_BUTTON
"""Default `Label` outline color"""

COLOR_FILL_CHECKBUTTON = COLOR_FILL_BUTTON
"""Default `CheckButton` fill color"""

COLOR_OUTLINE_CHECKBUTTON = COLOR_OUTLINE_BUTTON
"""Default `CheckButton` outline color"""

COLOR_FILL_TEXT = "#FFFFFF", "#FFFFFF", "#FFFFFF", "#E0E0E0"
"""Default `Text` fill color"""

COLOR_OUTLINE_TEXT = "#C0C0C0", "#414141", "#288CDB", "#D0D0D0"
"""Default `Text` outline color"""

COLOR_FILL_ENTRY = COLOR_FILL_TEXT
"""Default `Entry` fill color"""

COLOR_OUTLINE_ENTRY = COLOR_OUTLINE_TEXT
"""Default `Entry` outline color"""

COLOR_OUTLINE_PROGRESSBAR = COLOR_OUTLINE_TEXT
"""Default `ProgressBar` outline color"""

COLOR_FILL_PROGRESSBAR = "#E1E1E1", "#06b025"
"""Default `ProgressBar` fill color"""

COLOR_TEXT = "#000000", "#000000", "#000000", "#A3A3A3"
"""Default text color"""

COLOR_NONE = "", "", "", ""
"""Default transparent color tuple"""

COLOR_FILL_ON = "#288CDB", "#3E98DF", "#4884B4", "#E0E0E0"
"""Default fill color when `Switch` is on"""

COLOR_FILL_OFF = COLOR_FILL_BUTTON
"""Default fill color when `Switch` is off"""

COLOR_OUTLINE_ON = COLOR_FILL_ON
"""Default outline color when `Switch` is on"""

COLOR_OUTLINE_OFF = COLOR_OUTLINE_BUTTON
"""Default outline color when `Switch` is off"""

COLOR_FILL_SLIDER = '#000000', '#000000', '#000000', '#333333'
"""Default slider fill color"""

COLOR_OUTLINE_SLIDER = "#333333", "#333333", "#333333", "#666666"
"""Default slider outline color"""

# Other constants

BORDERWIDTH = 1
"""Default widget borderwidth"""

CURSOR = "│"
"""text cursor"""

FONT = "Microsoft YaHei" if SYSTEM == "Windows" else "DejaVu Sans" if SYSTEM == "linux" else "Arial"
"""Default font"""

SIZE = 20
"""Default font size"""

LIMIT = -1
"""Default widget text length limit"""

RADIUS = 0 if SYSTEM == "Windows" and int(platform.version()[-5:]) < 22000 else 4
"""Default widget fillet radius"""

FPS = 60
"""Default animation FPS"""

TICK = "✓"
"""Default checkbox symbol"""

CONTROL = lambda _: 1, 0, 1
"""Default control function"""

DURATION = 4000
"""Default ToolTip duration"""

TOOLTIP_FG = "black"
"""Default ToolTip foreground color"""

TOOLTIP_BG = "lightyellow"
"""Default ToolTip background color"""

TOOLTIP_HIGNLIGHT_THICKNESS = 1
"""Default ToolTip highlightthickness"""

TOOLTIP_HIGNLIGHT_BACKGROUND = "black"
"""Default ToolTip highlightbackground"""

SWITCH_WIDTH = 60
"""Default Switch width"""

SWITCH_HEIGHT = 30
"""Default Switch height"""

SWITCH_RADIUS = float("inf")
"""Default Switch radius"""

SWITCH_ANIMATION_MS = 250
"""Default animation duration of the Switch"""

# 3D constants

COLOR_FILL_POINT = "#000000"
"""Default point fill color"""

COLOR_OUTLINE_POINT = "#000000"
"""Default point outline color"""

COLOR_FILL_LINE = "#000000"
"""Default line fill color"""

COLOR_FILL_SIDE = ""
"""Default side fill color"""

COLOR_OUTLINE_SIDE = "#000000"
"""Default side outline color"""

POINT_SIZE = 1
"""Default point size"""

POINT_WIDTH = 1
"""Default point width"""

LINE_WDITH = 1
"""Default line width"""

SIDE_WIDTH = 1
"""Default side width"""

CAMERA_DISTANCE = 1000
"""Default 3D camera distance"""

ROTATE_CENTER = 0, 0, 0
"""Default rotation center"""

ORIGIN_COORDINATE = 0, 0, 0
"""Default origin coordinate"""

ORIGIN_SIZE = POINT_SIZE
"""Default origin size"""

ORIGIN_WIDTH = POINT_WIDTH
"""Default origin width"""

COLOR_FILL_ORIGIN = ""
"""Default origin fill color"""

COLOR_OUTLINE_ORIGIN = ""
"""Default origin outline color"""

all_constants = list(filter(lambda name: name.isupper(), globals()))
