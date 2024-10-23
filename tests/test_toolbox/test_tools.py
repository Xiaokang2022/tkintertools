# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest
import tkinter
import platform

from tkintertools.toolbox import tools


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = tkinter.Tk()

    def tearDown(self) -> None:
        self.tk.destroy()

    @unittest.skipUnless(
        platform.system() == "Windows", "This only work on Windows.")
    def test_func_get_hwnd(self) -> None:
        self.assertIsInstance(tools.get_hwnd(self.tk), int)


if __name__ == "__main__":
    unittest.main()
