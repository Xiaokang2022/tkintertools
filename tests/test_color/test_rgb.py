# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest
import tkinter


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = tkinter.Tk()

    def tearDown(self) -> None:
        self.tk.destroy()


if __name__ == "__main__":
    unittest.main()
