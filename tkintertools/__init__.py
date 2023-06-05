"""
tkintertools
============
The tkindertools module is an auxiliary module of the tkinder module.

Provides
--------
* Transparent, rounded and customized widgets
* Automatic control of picture size and widget size
* Scalable png pictures and playable gif pictures
* Regular mobile widgets and canvas interfaces
* Gradient colors and contrast colors
* Text with controllable length and alignment
* Convenient, inheritable singleton pattern class
* Display clear window and its contents

Contents
--------
* Container Widgets: `Tk`, `Toplevel`, `Canvas`
* Virtual Canvas Widgets: `Label`, `Button`, `CheckButton`, `Entry`, `Text`, `Progressbar`
* Tool Classes: `PhotoImage`, `Singleton`
* Tool Functions: `move`, `text`, `color`, `askfont`, `SetProcessDpiAwareness`

More
----
* GitCode: https://gitcode.net/weixin_62651706/tkintertools
* GitHub(Mirror): https://github.com/XiaoKang2022-CSDN/tkintertools
* Tutorials: https://xiaokang2022.blog.csdn.net/article/details/127374661
"""

import sys

if sys.version_info < (3, 7):  # Version Check
    error_info = '\n\033[31mOperation Requirements: \033[32m\nPython version shall not be less than\033[33m 3.7.0 !\033[0m'
    raise RuntimeError(error_info)

from .__main__ import (Button, Canvas, CheckButton, Entry, Label, PhotoImage,
                       Progressbar, SetProcessDpiAwareness, Singleton, Text,
                       Tk, Toplevel, askfont, color, move, text)
from .constants import (BACKGROUND, BORDERWIDTH, CFG_3D, COLOR_BAR,
                        COLOR_BUTTON_FILL, COLOR_BUTTON_OUTLINE,
                        COLOR_LINE_FILL, COLOR_NONE, COLOR_POINT_FILL,
                        COLOR_POINT_OUTLINE, COLOR_SIDE_FILL,
                        COLOR_SIDE_OUTLINE, COLOR_TEXT, COLOR_TEXT_FILL,
                        COLOR_TEXT_OUTLINE, CURSOR, FONT, FRAMES, LIMIT,
                        LINE_WDITH, POINT_SIZE, POINT_WIDTH,
                        PROCESS_SYSTEM_DPI_AWARE, RADIUS, SIDE_WIDTH, SIZE,
                        SYSTEM, TICK)

__author__ = 'Xiaokang2022<2951256653@qq.com>'
__version__ = '2.6.3'
__all__ = [
    # Container Widgets
    'Tk', 'Toplevel', 'Canvas',
    # Virtual Canvas Widgets
    'Label', 'Button', 'CheckButton', 'Entry', 'Text', 'Progressbar',
    # Tool Classes
    'PhotoImage', 'Singleton',
    # Tool Functions
    'move', 'text', 'color', 'askfont', 'SetProcessDpiAwareness',
    # Constants
    'SYSTEM', 'PROCESS_SYSTEM_DPI_AWARE', 'COLOR_BUTTON_FILL', 'COLOR_BUTTON_OUTLINE',
    'COLOR_TEXT_FILL', 'COLOR_TEXT_OUTLINE', 'COLOR_TEXT', 'COLOR_NONE', 'COLOR_BAR',
    'BACKGROUND', 'BORDERWIDTH', 'CURSOR', 'FONT', 'SIZE', 'LIMIT', 'RADIUS', 'FRAMES',
    'TICK', 'CFG_3D', 'COLOR_POINT_FILL', 'COLOR_POINT_OUTLINE', 'COLOR_LINE_FILL',
    'COLOR_SIDE_FILL', 'COLOR_SIDE_OUTLINE', 'POINT_SIZE', 'POINT_WIDTH', 'LINE_WDITH',
    'SIDE_WIDTH',
]
