# Copyright (c) 2022-2024 Xiaokang2022
# tkintertools is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at: http://license.coscl.org.cn/MulanPSL2.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

"""
tkt-designer
"""
import sys

from . import main

__author__ = "Xiaokang2022 <2951256653@qq.com>"
__version__ = "0.0.2"


def run(**kw) -> None:
    """Start tkt designer"""
    main.Application(*sys.argv[1:], **kw).root.mainloop()
