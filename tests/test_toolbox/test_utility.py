# pylint: disable=all

import pathlib
import platform
import tkinter
import unittest

from tkintertools.core import configs, containers
from tkintertools.toolbox import utility

try:
    import PIL
except ImportError:
    pass


class TestTrigger(unittest.TestCase):

    def setUp(self) -> None:
        self.t = utility.Trigger(lambda: None)

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
        self.tk = containers.Tk()

    def tearDown(self) -> None:
        self.tk.destroy()

    @unittest.skipUnless(platform.system() == "Windows", "This only work on Windows.")
    def test_get_hwnd(self) -> None:
        self.assertIsInstance(utility.get_parent(self.tk), int)

    @unittest.skipUnless(platform.system() == "Windows", "This only work on Windows.")
    def test_embed_window(self) -> None:
        toplevel = tkinter.Toplevel()
        self.assertIsNone(utility.embed_window(toplevel, self.tk))
        toplevel.destroy()

    @unittest.skipIf(platform.system() == "Darwin", "This not work on Darwin.")
    def test_load_font(self) -> None:
        self.assertFalse(utility.load_font(""))
        path = pathlib.Path(__file__).parent.parent/"assets/fonts/FiraCode.ttf"
        self.assertTrue(utility.load_font(str(path)))

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test_screen_size(self) -> None:
        self.assertIsInstance(utility.screen_size(), tuple)

    @unittest.skipUnless(platform.system() == "Windows", "This test only work on Windows.")
    def test_get_text_size(self) -> None:
        path = pathlib.Path(__file__).parent.parent/"assets/fonts/FiraCode.ttf"
        self.assertTrue(utility.load_font(str(path)))
        self.assertEqual(utility.get_text_size("", 20, "Fira Code"), (2, 24))
        self.assertEqual(utility.get_text_size(":)", 20, "Fira Code"), (26, 24))
        self.assertEqual(utility.get_text_size("\n", 20, "Fira Code"), (2, 48))
        self.assertEqual(utility.get_text_size("", 20, "Fira Code", padding=5), (12, 34))
        self.assertEqual(utility.get_text_size(":)"), utility.get_text_size(":)", configs.Font.size, configs.Font.family))

    def test_fix_cursor(self) -> None:
        self.assertEqual(utility.fix_cursor("a"), "a")

        disabled = utility.fix_cursor("disabled")

        match platform.system():
            case "Windows": self.assertEqual(disabled, "no")
            case "Darwin": self.assertEqual(disabled, "notallowed")
            case _: self.assertEqual(disabled, "arrow")

    def test_create_smoke(self) -> None:
        if globals().get("PIL") is None:
            raise unittest.SkipTest("PIL not available.")
        size = 100, 100
        smoke = utility.create_smoke(size)
        self.assertEqual((smoke.width(), smoke.height()), size)


if __name__ == "__main__":
    unittest.main()
