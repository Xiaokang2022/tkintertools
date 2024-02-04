# Copyright (c) 2022-2024 Xiaokang2022
# tkintertools is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at: http://license.coscl.org.cn/MulanPSL2.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

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
* `core`: Core codes of tkintertools
* `constants`: All constants
* `exceptions`: All exceptions
* `widgets`: All standard widgets
* `dialogs`: All standard dialogs
* `tools2d`: Support for 2d
* `tools3d`: Support for 3d
* `toolsmd`: Support for markdown

* designer: tkt-designer

If you want to know more information,
please see https://github.com/Xiaokang2022/tkintertools.
"""

import sys

if sys.version_info < (3, 10):
    raise ImportError("Python version requirement is 3.10 or higher.")

from .constants import *
from .core import *
from .widgets import *

__version__ = "3.0.0.dev7"
__author__ = "Xiaokang2022 <2951256653@qq.com>"
