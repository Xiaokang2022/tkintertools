"""
The `tkintertools` is a UI framework based on the `Canvas` class of `tkinter`.

* Homepage: https://xiaokang2022.github.io/tkintertools/
* GitHub: https://github.com/Xiaokang2022/tkintertools
* Gitee(Mirror): https://gitee.com/xiaokang-2022/tkintertools
* GitCode(Mirror): https://gitcode.com/Xiaokang2022/tkintertools

If you ❤️ this package, leave your ⭐ to me, thanks!

![Stars](https://img.shields.io/github/stars/Xiaokang2022/tkintertools?label=Stars&color=gold&logo=github&style=flat)
"""

# MIT License

# Copyright(c) 2022 Xiaokang2022

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import ctypes
import platform
import sys

if sys.version_info < (3, 10):
    raise ImportError(
        "tkintertools requires a Python version of 3.10 or greater.")

if platform.system() == "Windows":  # Set Windows DPI awareness
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

from .constants import *
from .core import *
from .standard import *

__version__ = "3.0.0.beta1"
__author__ = "Xiaokang2022 <2951256653@qq.com>"
