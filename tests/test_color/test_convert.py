# pylint: disable=all

import colorsys
import tkinter
import unittest

from maliang.color import convert


class TestCase(unittest.TestCase):

    def test_rgb_to_hex(self) -> None:
        self.assertEqual(convert.rgb_to_hex((255, 255, 255)), "#FFFFFF")
        self.assertEqual(convert.rgb_to_hex((0, 128, 0)), "#008000")

    def test_hex_to_rgb(self) -> None:
        self.assertEqual(convert.hex_to_rgb("#FFFFFF"), (255, 255, 255))
        self.assertEqual(convert.hex_to_rgb("#00ff00"), (0, 255, 0))
        self.assertEqual(convert.hex_to_rgb("#008000"), (0, 128, 0))

    def test_rgba_to_hex(self) -> None:
        self.assertEqual(convert.rgba_to_hex((255, 255, 255, 0)), "#FFFFFF00")
        self.assertEqual(convert.rgba_to_hex((0, 128, 0, 0.5)), "#00800080")

    def test_hex_to_rgba(self) -> None:
        self.assertEqual(convert.hex_to_rgba("#FFFFFF00"), (255, 255, 255, 0))
        self.assertEqual(convert.hex_to_rgba("#ffffFFff"), (255, 255, 255, 1))
        self.assertEqual(convert.hex_to_rgba("#008000ff"), (0, 128, 0, 1))
        self.assertAlmostEqual(convert.hex_to_rgba("#00000080")[-1], 0.5, 2)

    def test_rgb_to_rgba(self) -> None:
        self.assertEqual(convert.rgb_to_rgba((255, 255, 255)), (255, 255, 255, 0))

    def test_rgba_to_rgb(self) -> None:
        self.assertEqual(convert.rgba_to_rgb((0, 0, 0, 0), refer=(255, 255, 255)), (255, 255, 255))
        self.assertEqual(convert.rgba_to_rgb((0, 128, 0, 0.5), refer=(0, 0, 0)), (0, 64, 0))

    def test_hsl_to_rgb(self) -> None:
        self.assertEqual(convert.hsl_to_rgb((0, 0, 0)), (0, 0, 0))
        self.assertEqual(convert.hsl_to_rgb((0, 0.5, 0.5)), tuple(map(lambda x: round(x*255), colorsys.hls_to_rgb(0, 0.5, 0.5))))

    def test_rgb_to_hsl(self) -> None:
        self.assertEqual(convert.rgb_to_hsl((255, 255, 255)), (0, 1, 0))
        self.assertEqual(convert.rgb_to_hsl((127, 127, 127)), colorsys.rgb_to_hls(127/255, 127/255, 127/255))

    def test_hsl_to_hex(self) -> None:
        self.assertEqual(convert.hsl_to_hex((0, 0, 0)), "#000000")
        self.assertEqual(convert.hsl_to_hex((0, 0.5, 0.5)), convert.rgb_to_hex(convert.hsl_to_rgb((0, 0.5, 0.5))))

    def test_hex_to_hsl(self) -> None:
        self.assertEqual(convert.hex_to_hsl("#FFFFFF"), (0, 1, 0))
        self.assertEqual(convert.hex_to_hsl("#808080"), colorsys.rgb_to_hls(128/255, 128/255, 128/255))

    def test_name_to_rgb(self) -> None:
        self.assertEqual(convert.name_to_rgb("white"), (255, 255, 255))
        self.assertEqual(convert.name_to_rgb("green"), (0, 128, 0))

        with self.assertRaises(tkinter.TclError):
            convert.name_to_rgb("歪比八卜")

    def test_rgb_to_name(self) -> None:
        self.assertEqual(convert.rgb_to_name((255, 255, 255)), ["gray100", "grey100", "white"])
        self.assertEqual(convert.rgb_to_name((0, 128, 0)), ["green"])

    def test_name_to_hex(self) -> None:
        self.assertEqual(convert.name_to_hex("white"), "#FFFFFF")
        self.assertEqual(convert.name_to_hex("green"), "#008000")

    def test_hex_to_name(self) -> None:
        self.assertEqual(convert.hex_to_name("#FFFFFF"), ["gray100", "grey100", "white"])
        self.assertEqual(convert.hex_to_name("#008000"), ["green"])

    def test_fix_hex_length(self) -> None:
        self.assertEqual(convert.fix_hex_length("#FFF"), "#FFFFFF")
        self.assertEqual(convert.fix_hex_length("#00ff00"), "#00ff00")  
        self.assertEqual(convert.fix_hex_length("#00ff"), "#0000ffff")  

    def test_str_to_rgb(self) -> None:
        self.assertEqual(convert.str_to_rgb("#FFFFFF"), (255, 255, 255))
        self.assertEqual(convert.str_to_rgb("#00ff00"), (0, 255, 0))
        self.assertEqual(convert.str_to_rgb("Blue"), (0, 0, 255))


if __name__ == "__main__":
    unittest.main()
