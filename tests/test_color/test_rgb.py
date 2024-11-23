# pylint: disable=all

import platform
import unittest

from tkintertools.color import rgb


class Test(unittest.TestCase):

    def test_contrast(self) -> None:
        self.assertEqual(rgb.contrast((0, 0, 0)), (255, 255, 255))
        self.assertEqual(rgb.contrast((0, 127, 255)), (255, 128, 0))
        self.assertEqual(rgb.contrast((1, 0, 0), channels=(False, True, True)),
                         (1, 255, 255))

    def test_convert(self) -> None:
        self.assertEqual(
            rgb.convert((0, 0, 0), (255, 255, 255), 0.5), (128, 128, 128))
        self.assertEqual(rgb.convert((0, 127, 255), (255, 127, 0),
                         0.5, channels=(False, True, True)), (0, 127, 127))

    def test_blend(self) -> None:
        self.assertEqual(
            rgb.blend([(0, 0, 0), (255, 255, 255)]), (128, 128, 128))
        self.assertEqual(
            rgb.blend([(0, 0, 0), (100, 100, 100)], weights=(3, 7)),
            (70, 70, 70))

    def test_gradient(self) -> None:
        self.assertEqual(
            rgb.gradient((0, 0, 0), (100, 100, 100), 3, 0.6),
            [(0, 0, 0), (20, 20, 20), (40, 40, 40)])
        self.assertEqual(
            rgb.gradient((0, 0, 0), (100, 100, 100), 2, contoller=lambda _: 1),
            [(100, 100, 100), (100, 100, 100)])
        self.assertEqual(rgb.gradient((0, 0, 0), (100, 100, 100), 2, channels=(
            True, True, False)), [(0, 0, 0), (50, 50, 0)])

    def test_str_to_rgb(self) -> None:
        self.assertIs(rgb.str_to_rgb, rgb.str2rgb)
        self.assertEqual(rgb.str_to_rgb("#FFFFFF"), (255, 255, 255))
        self.assertEqual(rgb.str_to_rgb("#00ff00"), (0, 255, 0))

        if platform.system() == "Linux":
            raise unittest.SkipTest("No display name")

        self.assertEqual(rgb.str_to_rgb("Blue"), (0, 0, 255))

    def test_rgb_to_str(self) -> None:
        self.assertIs(rgb.rgb_to_str, rgb.rgb2str)
        self.assertEqual(rgb.rgb_to_str((0, 0, 0)), "#000000")

    def test__str_to_rgba(self) -> None:
        self.assertIs(rgb.str_to_rgba, rgb.str2rgba)
        self.assertEqual(
            rgb.str_to_rgba("#00000000", reference="#FFFFFF"),
            (255, 255, 255))
        self.assertEqual(
            rgb.str_to_rgba("#12345678", reference="#000000"),
            (8, 24, 40))

    def test_MAX(self) -> None:
        self.assertEqual(rgb.MAX, (255, 255, 255))

    def test_RGB(self) -> None:
        self.assertEqual(rgb.RGB, tuple[int, int, int])


if __name__ == "__main__":
    unittest.main()
