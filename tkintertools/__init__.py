# Copyright (c) 2022 Xiaokang2022
# tkintertools is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at: http://license.coscl.org.cn/MulanPSL2.
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
* Convenient, inheritable singleton pattern class
* 3D drawing

Contents
--------
* Container Widgets: `Tk`, `Toplevel`, `Canvas`
* Virtual Canvas Widgets: `Label`, `Button`, `CheckButton`, `Entry`, `Text`, `Progressbar`,`ToolTip`, `Switch`
* Tool Functions: `color`, `askfont`, `SetProcessDpiAwareness`
* Tool Classes: `PhotoImage`, `Animation`
* Tool Submodules: `tool_3d`

More
----
[GitHub](https://github.com/Xiaokang2022/tkintertools) ·
[License](https://github.com/Xiaokang2022/tkintertools/blob/master/LICENSE.txt) ·
[ChangeLog](https://github.com/Xiaokang2022/tkintertools/blob/master/CHANGELOG.md) ·
[Wiki](https://github.com/Xiaokang2022/tkintertools/wiki)
"""

import sys  # Get interpreter version information

if sys.version_info < (3, 8):  # Version Check
    err_info = 'Python version is too low (>=3.8)'
    raise RuntimeError(err_info)

from .__main__ import *
from .constants import *

__author__ = 'Xiaokang2022<2951256653@qq.com>'
__version__ = '2.6.10.dev1'
__all__ = [
    # Container Widgets
    'Tk', 'Toplevel', 'Canvas',
    # Virtual Canvas Widgets
    'Label', 'Button', 'CheckButton', 'Entry', 'Text', 'Progressbar', 'ToolTip', 'Switch',
    # Tool Classes
    'PhotoImage', 'Animation',
    # Tool Functions
    'color', 'askfont', 'SetProcessDpiAwareness',
] + all_constants
