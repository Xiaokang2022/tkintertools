""" All constants """

import sys

PROCESS_SYSTEM_DPI_AWARE = 1
""" default DPI aware """


COLOR_BUTTON_FILL = '#E1E1E1', '#E5F1FB', '#CCE4F7', '#E0E0E0'
""" default button fill color """

COLOR_BUTTON_OUTLINE = '#C0C0C0', '#288CDB', '#4884B4', '#D0D0D0'
""" default button outline color """

COLOR_TEXT_FILL = '#FFFFFF', '#FFFFFF', '#FFFFFF', '#E0E0E0'
""" default text widget fill color """

COLOR_TEXT_OUTLINE = '#C0C0C0', '#414141', '#288CDB', '#D0D0D0'
""" default text widget outline color """

COLOR_TEXT = '#000000', '#000000', '#000000', '#A3A3A3'
""" default text color """

COLOR_NONE = '', '', '', ''
""" default transparent color tuple """

COLOR_BAR = '#E1E1E1', '#06b025'
""" default progress bar color """

BACKGROUND = '#F1F1F1'
""" default Canvas background color """


BORDERWIDTH = 1
""" default widget borderwidth """

CURSOR = '│'
""" text cursor """

FONT = 'Microsoft YaHei' if sys.platform == 'win32' else 'DejaVu Sans' if sys.platform == 'linux' else 'Arial'
""" default font """

SIZE = 20
""" default font size """

LIMIT = -1
""" default widget text length limit """

RADIUS = 0
""" default widget fillet radius """

FRAMES = 60
""" default move frame rate """

TICK = '✓'
""" default checkbox symbol """
