"""
tkintertools is an auxiliary development module of the Python3 built-in module tkinter.

Provides
--------
* Transparent, rounded and customized widgets
* Automatic control of picture size and widget size
* Scalable png pictures and playable gif pictures
* Regular mobile widgets and canvas interfaces
* Gradient colors and contrast colors
* Default aesthetic widgets
* Extra useful widgets
* 3D drawing

Contents
--------
* `_tools`: Some utility functions
* `color`: Support about color
* `constants`: All constants
* `core`: Core codes of tkintertools
* `dialogs`: All standard Dialogs
* `exceptions`: All exceptions
* `features`: All standard Features
* `images`: All standard Images
* `shapes`: All standard Shapes
* `texts`: All standard Texts
* `tool2d`: Support for 2D
* `tool3d`: Support for 3D
* `toolgm`: Support for Game
* `toolmd`: Support for Markdown
* `widgets`: All standard Widgets

* designer: tkt-designer

If you want to know more information,
please see https://github.com/Xiaokang2022/tkintertools.
"""

# Copyright (c) 2022-2024 Xiaokang2022
# tkintertools is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at: http://license.coscl.org.cn/MulanPSL2.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import sys

if sys.version_info < (3, 10):
    raise ImportError("Python version requirement is 3.12 or higher.")

from .constants import *
from .core import *
from .widgets import *

__version__ = "3.0.0.alpha3"
__author__ = "Xiaokang2022 <2951256653@qq.com>"
