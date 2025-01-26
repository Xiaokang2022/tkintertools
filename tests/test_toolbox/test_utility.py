# pylint: disable=all

import contextlib
import importlib
import io
import pathlib
import platform
import tkinter
import unittest
import unittest.mock

import maliang
from maliang.core import configs, containers
from maliang.toolbox import utility


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


class TestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = containers.Tk()
        self.cv = containers.Canvas(self.tk)

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
        with io.StringIO() as captured_output:
            with contextlib.redirect_stderr(captured_output):
                self.assertFalse(utility.load_font(""))

        path = pathlib.Path(__file__).parent.parent/"assets/fonts/FiraCode.ttf"
        self.assertTrue(utility.load_font(str(path)))
        self.assertTrue(utility.load_font(bytes(path)))

        with unittest.mock.patch("sys.platform", "darwin"):
            self.assertFalse(utility.load_font(str(path)))

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

        widget = maliang.Button(self.cv, (0, 0))
        self.assertEqual(utility.get_text_size("", 20, "Fira Code", master=widget), (2, 24))

    def test_fix_cursor(self) -> None:
        self.assertEqual(utility.fix_cursor("a"), "a")

        with unittest.mock.patch("platform.system", return_value="Windows"):
            self.assertEqual(utility.fix_cursor("disabled"), "no")

        with unittest.mock.patch("platform.system", return_value="Darwin"):
            self.assertEqual(utility.fix_cursor("disabled"), "notallowed")

        with unittest.mock.patch("platform.system", return_value="Linux"):
            self.assertEqual(utility.fix_cursor("disabled"), "arrow")

    def test_create_smoke(self) -> None:
        size = 100, 100
        smoke = utility.create_smoke(size)
        self.assertEqual((smoke.width(), smoke.height()), size)

        with unittest.mock.patch.dict("sys.modules", {'PIL': None}):
            importlib.reload(utility)

        self.assertRaises(RuntimeError, utility.create_smoke, size)

        importlib.reload(utility)


if __name__ == "__main__":
    unittest.main()
