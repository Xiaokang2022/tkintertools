# Copyright (c) 2022-2023 Xiaokang2022
# tkintertools is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at: http://license.coscl.org.cn/MulanPSL2.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

"""
tkintertools
------------
tkintertools is an auxiliary development module of the Python3 built-in module tkinter.

Provides: 
* Transparent, rounded and customized widgets
* Automatic control of picture size and widget size
* Scalable png pictures and playable gif pictures
* Regular mobile widgets and canvas interfaces
* Gradient colors and contrast colors
* Convenient, inheritable singleton pattern class
* 3D drawing

If you want to know more information,
please see https://github.com/Xiaokang2022/tkintertools.
"""

import ctypes
import platform
import sys

if sys.version_info < (3, 11):
    error_info = 'Python version is too low (>=3.11)'
    raise RuntimeError(error_info)

if platform.system() == 'Windows':
    if platform.win32_ver() == '6.1':  # Windows 7
        ctypes.windll.user32.SetProcessDPIAware()
    else:
        ctypes.WinDLL('shcore').SetProcessDpiAwareness(1)

from .constants import *
from .core import *
from .exceptions import *
from .widgets import *

__author__ = 'Xiaokang2022<2951256653@qq.com>'
__version__ = '3.0.0.dev0'
