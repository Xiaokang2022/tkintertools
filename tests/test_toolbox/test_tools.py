# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import pathlib
import platform
import tkinter
import unittest

from tkintertools.toolbox import tools


class TestTrigger(unittest.TestCase):

    def setUp(self) -> None:
        self.t = tools.Trigger(lambda: None)

    def test_update(self) -> None:
        self.t.reset()
        self.assertFalse(self.t.get())
        self.t.update(False)
        self.assertFalse(self.t.get())
        self.t.update()
        self.assertTrue(self.t.get())
        self.t.update(False)
        self.assertTrue(self.t.get())

    def test_lock(self) -> None:
        self.t.reset()
        self.t.lock()
        self.t.update()
        self.assertFalse(self.t.get())
        self.t.unlock()
        self.t.update()
        self.assertTrue(self.t.get())


class Test(unittest.TestCase):

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def setUp(self) -> None:
        self.tk = tkinter.Tk()

    def tearDown(self) -> None:
        self.tk.destroy()

    @unittest.skipUnless(
        platform.system() == "Windows", "This only work on Windows.")
    def test_get_hwnd(self) -> None:
        self.assertIsInstance(tools.get_hwnd(self.tk), int)

    @unittest.skipUnless(
        platform.system() == "Windows", "This only work on Windows.")
    def test_embed_window(self) -> None:
        toplevel = tkinter.Toplevel()
        self.assertIsNone(tools.embed_window(toplevel, self.tk))
        toplevel.destroy()

    @unittest.skipIf(platform.system() == "Darwin", "This not work on Darwin.")
    def test_load_font(self) -> None:
        self.assertFalse(tools.load_font(""))
        path = pathlib.Path(__file__).parent.parent/"assets/fonts/FiraCode.ttf"
        self.assertTrue(tools.load_font(str(path)))

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test_screen_size(self) -> None:
        self.assertIsInstance(tools.screen_size(), tuple)

    @unittest.skipUnless(
        platform.system() == "Windows", "This only work on Windows.")
    def test_set_mouse_position(self) -> None:
        self.assertIsNone(tools.set_mouse_position(0, 0))

    @unittest.skipUnless(
        platform.system() == "Windows", "This test only work on Windows.")
    def test_get_text_size(self) -> None:
        path = pathlib.Path(__file__).parent.parent/"assets/fonts/FiraCode.ttf"
        self.assertTrue(tools.load_font(str(path)))
        self.assertEqual(tools.get_text_size("", 20, "Fira Code"), (2, 24))
        self.assertEqual(tools.get_text_size(":)", 20, "Fira Code"), (26, 24))
        self.assertEqual(tools.get_text_size("\n", 20, "Fira Code"), (2, 48))
        self.assertEqual(tools.get_text_size(
            "", 20, "Fira Code", padding=5), (12, 34))


if __name__ == "__main__":
    unittest.main()
