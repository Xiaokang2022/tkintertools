"""
tkintertools is an auxiliary development module of the Python3 built-in module tkinter.

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

if sys.version_info < (3, 12):
    raise ImportError("Python version requirement is 3.12 or higher.")

from .constants import *
from .core import *
from .extra.widgets_ex import *
from .stdandard.widgets import *

__version__ = "3.0.0.alpha4"
__author__ = "Xiaokang2022 <2951256653@qq.com>"
