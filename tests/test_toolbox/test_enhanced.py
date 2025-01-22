# pylint: disable=all

import importlib
import pathlib
import unittest
import unittest.mock

from maliang.core import containers
from maliang.toolbox import enhanced


class TestPhotoImage(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = containers.Tk()
        self.image = enhanced.PhotoImage(file=pathlib.Path(__file__).parent.parent/"assets/images/logo.png")
        self.width = self.image.width()
        self.height = self.image.height()

    def tearDown(self) -> None:
        self.tk.destroy()

    def test_scale(self) -> None:
        large_image = self.image.scale(1.5, 1.5)
        small_image = self.image.scale(0.5, 0.5)
        large_width = large_image.width()
        large_height = large_image.height()
        small_width = small_image.width()
        small_height = small_image.height()
        self.assertEqual(large_width, self.width*1.5)
        self.assertEqual(large_height, self.height*1.5)
        self.assertEqual(small_width, self.width*0.5)
        self.assertEqual(small_height, self.height*0.5)

    def test_resize(self) -> None:
        new_image = self.image.resize(100, 100)
        new_width = new_image.width()
        new_height = new_image.height()
        self.assertEqual(new_width, 100)
        self.assertEqual(new_height, 100)


class TestPhotoImageNoPillow(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = containers.Tk()

        with unittest.mock.patch.dict("sys.modules", {'PIL': None}):
            importlib.reload(enhanced)

        self.image = enhanced.PhotoImage(file=pathlib.Path(__file__).parent.parent/"assets/images/logo.png")
        self.width = self.image.width()
        self.height = self.image.height()

    def tearDown(self) -> None:
        importlib.reload(enhanced)
        self.tk.destroy()

    def test_scale(self) -> None:
        large_image = self.image.scale(1.5, 1.5)
        small_image = self.image.scale(0.5, 0.5)
        large_width = large_image.width()
        large_height = large_image.height()
        small_width = small_image.width()
        small_height = small_image.height()
        self.assertEqual(large_width, self.width*1.5)
        self.assertEqual(large_height, self.height*1.5)
        self.assertEqual(small_width, self.width*0.5)
        self.assertEqual(small_height, self.height*0.5)

    def test_resize(self) -> None:
        new_image = self.image.resize(100, 100)
        new_width = new_image.width()
        new_height = new_image.height()
        self.assertEqual(new_width, 100)
        self.assertEqual(new_height, 100)


if __name__ == "__main__":
    unittest.main()
