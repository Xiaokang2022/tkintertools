# Copyright (c) 2022 Xiaokang2022
# tkintertools is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at: http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

"""
tkintertools
============
The tkintertools module is an auxiliary module of the tkinter module.

Provides
--------
* Transparent, rounded and customized widgets
* Automatic control of picture size and widget size
* Scalable png pictures and playable gif pictures
* Regular mobile widgets and canvas interfaces
* Gradient colors and contrast colors
* Text with controllable length and alignment
* Convenient, inheritable singleton pattern class
* 3D drawing

Contents
--------
* Container Widgets: `Tk`, `Toplevel`, `Canvas`
* Virtual Canvas Widgets: `Label`, `Button`, `CheckButton`, `Entry`, `Text`, `Progressbar`
* Tool Classes: `PhotoImage`, `Singleton`
* Tool Functions: `move`, `text`, `color`, `askfont`, `SetProcessDpiAwareness`
* Tool Submodules: `tool_3d`

More
----
* GitHub: https://github.com/Xiaokang2022/tkintertools
* License: https://github.com/Xiaokang2022/tkintertools/blob/master/LICENSE.txt
* ChangeLog: https://github.com/Xiaokang2022/tkintertools/blob/master/CHANGELOG.md
"""

import sys

if sys.version_info < (3, 8):  # Version Check
    error_info = '\n\033[31mOperation Requirements: \033[32m\nPython version shall not be less than\033[33m 3.8 !\033[0m'
    raise RuntimeError(error_info)

from .__main__ import (Button, Canvas, CheckButton, Entry, Label, PhotoImage,
                       Progressbar, SetProcessDpiAwareness, Singleton, Text,
                       Tk, Toplevel, askfont, color, move, text)
from .constants import *

__author__ = 'Xiaokang2022<2951256653@qq.com>'
__version__ = '2.6.6'
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
    'BORDERWIDTH', 'CURSOR', 'FONT', 'SIZE', 'LIMIT', 'RADIUS', 'FRAMES', 'TICK', 'CFG_3D',
    'COLOR_POINT_FILL', 'COLOR_POINT_OUTLINE', 'COLOR_LINE_FILL', 'COLOR_SIDE_FILL',
    'COLOR_SIDE_OUTLINE', 'POINT_SIZE', 'POINT_WIDTH', 'LINE_WDITH', 'SIDE_WIDTH',
]
