# pylint: disable=all

import unittest

from maliang.color import rgb


class TestCase(unittest.TestCase):

    def test_contrast(self) -> None:
        self.assertEqual(rgb.contrast((0, 0, 0)), (255, 255, 255))
        self.assertEqual(rgb.contrast((0, 127, 255)), (255, 128, 0))
        self.assertEqual(rgb.contrast((1, 0, 0), channels=(False, True, True)), (1, 255, 255))

    def test_transition(self) -> None:
        self.assertEqual(rgb.transition((0, 0, 0), (255, 255, 255), 0.5), (128, 128, 128))
        self.assertEqual(rgb.transition((0, 127, 255), (255, 127, 0), 0.5, channels=(False, True, True)), (0, 127, 127))

    def test_blend(self) -> None:
        self.assertEqual(rgb.blend((0, 0, 0), (255, 255, 255)), (128, 128, 128))
        self.assertEqual(rgb.blend((0, 0, 0), (100, 100, 100), weights=[3, 7]), (70, 70, 70))

    def test_gradient(self) -> None:
        self.assertEqual(rgb.gradient((0, 0, 0), (100, 100, 100), 3, 0.6), [(0, 0, 0), (20, 20, 20), (40, 40, 40)])
        self.assertEqual(rgb.gradient((0, 0, 0), (100, 100, 100), 2, contoller=lambda _: 1), [(100, 100, 100), (100, 100, 100)])
        self.assertEqual(rgb.gradient((0, 0, 0), (100, 100, 100), 2, channels=(True, True, False)), [(0, 0, 0), (50, 50, 0)])


if __name__ == "__main__":
    unittest.main()
