""" All constants """

import sys

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

BACKGROUND = '#F1F1F1'
""" Default Canvas background color """


BORDERWIDTH = 1
""" Default widget borderwidth """

CURSOR = '│'
""" text cursor """

FONT = 'Microsoft YaHei' if sys.platform == 'win32' else 'DejaVu Sans' if sys.platform == 'linux' else 'Arial'
""" Default font """

SIZE = 20
""" Default font size """

LIMIT = -1
""" Default widget text length limit """

RADIUS = 0
""" Default widget fillet radius """

FRAMES = 60
""" Default move frame rate """

TICK = '✓'
""" Default checkbox symbol """


CFG_3D = 500, None, None
""" Default 3D configuration """
