# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest
import tkinter

from tkintertools.color import colormap


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = tkinter.Tk()

    def tearDown(self) -> None:
        self.tk.destroy()

    def test_function_name_to_rgb(self) -> None:
        self.assertIs(colormap.name_to_rgb, colormap.name2rgb)
        self.assertEqual(colormap.name_to_rgb("blue"), (0, 0, 255))
        self.assertEqual(colormap.name_to_rgb("BLUE"), (0, 0, 255))
        self.assertEqual(colormap.name_to_rgb("#00F"), (0, 0, 65535))
        self.assertEqual(colormap.name_to_rgb("#0000FF"), (0, 0, 65535))
        self.assertEqual(colormap.name_to_rgb("#000000FFF"), (0, 0, 65535))
        self.assertEqual(colormap.name_to_rgb("#00000000FFFF"), (0, 0, 65535))
        self.assertRaises(tkinter.TclError, colormap.name_to_rgb, "XXX")
        self.assertRaises(
            tkinter.TclError, colormap.name_to_rgb, "#0000000000FFFFF")


if __name__ == "__main__":
    unittest.main()
