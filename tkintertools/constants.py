"""All constants"""

import platform

FONT = "Microsoft YaHei" if platform.system() == "Windows" else "Arial"
"""Default font"""

SIZE = -24
"""Default font size"""

IS_WIN10 = platform.system() == "Windows" and int(
    platform.version()[-5:]) < 22000

# IS_WIN10 = not IS_WIN10

# 3D constants

COLOR_FILL_POINT = "#000000"
"""Default `Point` fill color"""

COLOR_OUTLINE_POINT = "#000000"
"""Default `Point` outline color"""

COLOR_FILL_LINE = "#000000"
"""Default `Line` fill color"""

COLOR_FILL_SIDE = ""
"""Default `Side` fill color"""

COLOR_OUTLINE_SIDE = "#000000"
"""Default `Side` outline color"""

POINT_SIZE = 1
"""Default `Point` size"""

POINT_WIDTH = 1
"""Default `Point` width"""

LINE_WIDTH = 1
"""Default `Line` width"""

SIDE_WIDTH = 1
"""Default `Side` width"""

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
