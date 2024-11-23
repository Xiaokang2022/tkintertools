# pylint: disable=all

import colorsys
import math
import unittest

from tkintertools.color import hsl


class Test(unittest.TestCase):

    def test_contrast(self) -> None:
        self.assertEqual(hsl.contrast((1, 1, 1)), (math.tau - 1, 0, 0))
        self.assertEqual(hsl.contrast(
            (1, 1, 1), channels=(False, True, True)), (1, 0, 0))

    def test_convert(self) -> None:
        self.assertEqual(hsl.convert(
            (0, 0, 0), (math.tau, 1, 1), 0.5), (math.pi, 0.5, 0.5))
        self.assertEqual(hsl.convert((0, 0, 0), (math.pi, 1, 1),
                         1, channels=(True, True, False)), (math.pi, 1, 0))

    def test_blend(self) -> None:
        self.assertEqual(hsl.blend([(0, 0, 0), (1, 1, 1)]), (0.5, 0.5, 0.5))
        self.assertEqual(
            hsl.blend([(0, 0, 0), (1, 1, 1)], weights=(4, 6)), (0.6, 0.6, 0.6))

    def test_gradient(self) -> None:
        list_1 = hsl.gradient((0, 0, 0), (1, 1, 1), 3, 0.6)
        list_2 = [(0, 0, 0), (0.2, 0.2, 0.2), (0.4, 0.4, 0.4)]

        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(list_1[i][j], list_2[i][j])

        self.assertEqual(
            hsl.gradient((0, 0, 0), (1, 1, 1), 2, contoller=lambda _: 1),
            [(1, 1, 1), (1, 1, 1)])
        self.assertEqual(hsl.gradient((0, 0, 0), (1, 1, 1), 2, channels=(
            True, True, False)), [(0, 0, 0), (0.5, 0.5, 0)])

    def test_hsl_to_rgb(self) -> None:
        self.assertIs(hsl.hsl_to_rgb, hsl.hsl2rgb)
        self.assertEqual(hsl.hsl_to_rgb((0, 0, 0)), (0, 0, 0))
        self.assertEqual(hsl.hsl_to_rgb((0, 0.5, 0.5)), tuple(
            map(lambda x: round(x*255), colorsys.hls_to_rgb(0, 0.5, 0.5))))

    def test_rgb_to_hsl(self) -> None:
        self.assertIs(hsl.rgb_to_hsl, hsl.rgb2hsl)
        self.assertEqual(hsl.rgb_to_hsl((255, 255, 255)), (0, 1, 0))
        self.assertEqual(hsl.rgb_to_hsl((127, 127, 127)),
                         colorsys.rgb_to_hls(127/255, 127/255, 127/255))

    def test_MAX(self) -> None:
        self.assertEqual(hsl.MAX, (math.tau, 1, 1))

    def test_HSL(self) -> None:
        self.assertEqual(hsl.HSL, tuple[float, float, float])


if __name__ == "__main__":
    unittest.main()
