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
* Container Widget: `Tk`, `Toplevel`, `Canvas`
* Virtual Widget: `Label`, `Button`, `Entry`, `Text`, `Progressbar`
* Tool Class: `PhotoImage`, `Singleton`
* Tool Function: `move`, `text`, `color`, `SetProcessDpiAwareness`

More
----
* GitCode: https://gitcode.net/weixin_62651706/tkintertools
* GitHub(Mirror): https://github.com/XiaoKang2022-CSDN/tkintertools
* Tutorials: https://xiaokang2022.blog.csdn.net/article/details/127374661
"""

import sys  # 检测 Python 版本

if sys.version_info < (3, 10):
    # 版本检测，低版本缺失部分语法
    error_info = '\n\033[31mOperation Requirements: \033[32m\nPython version shall not be less than\033[33m 3.10.0!\033[0m'
    raise RuntimeError(error_info)

from .__main__ import *

__author__ = 'Xiaokang2022<2951256653@qq.com>'
__version__ = '2.5.12'
__all__ = [
    'Tk', 'Toplevel', 'Canvas',
    'Label', 'Button', 'Entry', 'Text', 'Progressbar',
    'PhotoImage', 'Singleton',
    'move', 'text', 'color', 'SetProcessDpiAwareness'
]
