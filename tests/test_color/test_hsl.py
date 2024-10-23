# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest
import platform
import math

from tkintertools.color import hsl


class Test(unittest.TestCase):

    def test_function(self) -> None:
        self.assertEqual(hsl.contrast((1, 1, 1)), (math.tau - 1, 0, 0))

    def test_constant_MAX(self) -> None:
        self.assertEqual(hsl.MAX, (math.tau, 1, 1))

    def test_type_HSL(self) -> None:
        self.assertEqual(hsl.HSL, tuple[float, float, float])


if __name__ == "__main__":
    unittest.main()
