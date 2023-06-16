""" All constants """

import platform

SYSTEM = platform.system()
""" Operating System """

PROCESS_SYSTEM_DPI_AWARE = 1
""" Default DPI aware """


COLOR_BUTTON_FILL = '#E1E1E1', '#E5F1FB', '#CCE4F7', '#E0E0E0'
""" Default button fill color """

COLOR_BUTTON_OUTLINE = '#C0C0C0', '#288CDB', '#4884B4', '#D0D0D0'
""" Default button outline color """

COLOR_TEXT_FILL = '#FFFFFF', '#FFFFFF', '#FFFFFF', '#E0E0E0'
""" Default text widget fill color """

COLOR_TEXT_OUTLINE = '#C0C0C0', '#414141', '#288CDB', '#D0D0D0'
""" Default text widget outline color """

COLOR_TEXT = '#000000', '#000000', '#000000', '#A3A3A3'
""" Default text color """

COLOR_NONE = '', '', '', ''
""" Default transparent color tuple """

COLOR_BAR = '#E1E1E1', '#06b025'
""" Default progress bar color """


BORDERWIDTH = 1
""" Default widget borderwidth """

CURSOR = '│'
""" text cursor """

FONT = 'Microsoft YaHei' if SYSTEM == 'Windows' else 'DejaVu Sans' if SYSTEM == 'linux' else 'Arial'
""" Default font """

SIZE = 20
""" Default font size """

LIMIT = -1
""" Default widget text length limit """

RADIUS = 0 if SYSTEM == 'Windows' and int(
    platform.version()[-5:]) < 22000 else 4
""" Default widget fillet radius """

FRAMES = 60
""" Default move frame rate """

TICK = '✓'
""" Default checkbox symbol """


CAMERA_DISTANCE = 1000
""" Default 3D camera distance """


COLOR_POINT_FILL = '#000000'
""" Default point fill color """

COLOR_POINT_OUTLINE = '#000000'
""" Default point outline color """

COLOR_LINE_FILL = '#000000'
""" Default line fill color """

COLOR_SIDE_FILL = ''
""" Default side fill color """

COLOR_SIDE_OUTLINE = '#000000'
""" Default side outline color """

POINT_SIZE = 1
""" Default point size """

POINT_WIDTH = 1
""" Default point width """

LINE_WDITH = 1
""" Default line width """

SIDE_WIDTH = 1
""" Default side width """


__all__ = [name for name in globals() if name.isupper()]
