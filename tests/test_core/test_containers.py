# pylint: disable=all

import contextlib
import io
import unittest
import unittest.mock

from tkintertools.core import containers
from tkintertools.standard import widgets


class TestTk(unittest.TestCase):

    def test_init(self) -> None:
        containers.Tk(icon="").destroy()
        containers.Tk(icon="tests/assets/images/logo.ico").destroy()
        containers.Tk(title=":)").destroy()

        with unittest.mock.patch("platform.system", return_value="Darwin"):
            containers.Tk(icon="tests/assets/images/logo.ico").destroy()

    def test_ratios(self) -> None:
        with containers.Tk() as tk:
            self.assertEqual(tk.ratios, (1., 1.))
            tk.wm_geometry(f"{tk.size[0]//2}x{tk.size[1]//2}")
            tk.update_idletasks()
            tk._zoom()
            self.assertEqual(tk.ratios, (0.5, 0.5))

    def test_alpha(self) -> None:
        with containers.Tk() as tk:
            self.assertEqual(tk.alpha(), 1.)
            self.assertIsNone(tk.alpha(0.8))
            self.assertEqual(tk.alpha(), 0.8)

    def test_topmost(self) -> None:
        with containers.Tk() as tk:
            self.assertIsNone(tk.topmost())
            self.assertTrue(tk.topmost(None))
            self.assertIsNone(tk.topmost(False))
            self.assertFalse(tk.topmost(None))

    def test_fullscreen(self) -> None:
        with containers.Tk() as tk:
            self.assertIsNone(tk.fullscreen())
            self.assertTrue(tk.fullscreen(None))
            self.assertIsNone(tk.fullscreen(False))
            self.assertFalse(tk.fullscreen(None))

    def test_toolwindow(self) -> None:
        with containers.Tk() as tk:
            self.assertIsNone(tk.toolwindow())
            self.assertTrue(tk.toolwindow(None))
            self.assertIsNone(tk.toolwindow(False))
            self.assertFalse(tk.toolwindow(None))

    def test_transparentcolor(self) -> None:
        with containers.Tk() as tk:
            self.assertEqual(tk.transparentcolor(), None)
            self.assertIsNone(tk.transparentcolor("red"))
            self.assertEqual(tk.transparentcolor(), "red")
            self.assertIsNone(tk.transparentcolor(""))
            self.assertEqual(tk.transparentcolor(), None)

    def test_center(self) -> None:
        with containers.Tk() as tk:
            tk.center()
            with containers.Toplevel() as tl:
                tl.center(refer=tk)

    def test_theme(self) -> None:
        with containers.Tk() as tk:
            with containers.Toplevel(tk):
                with containers.Canvas(tk):
                    tk.theme(True, include_children=True, include_canvases=True)

    def test_at_exit(self) -> None:
        a = None

        def command() -> None:
            nonlocal a
            a = True

        with containers.Tk() as tk:
            tk.at_exit(command, ensure_destroy=False)
            tk.call(tk.wm_protocol("WM_DELETE_WINDOW"))

        self.assertTrue(a)

        tk = containers.Tk()  # NOTE: This does not need to be destroyed again
        tk.at_exit(lambda: None)
        tk.call(tk.wm_protocol("WM_DELETE_WINDOW"))

        def callback_raise() -> None:
            raise RuntimeError

        with io.StringIO() as captured_output:
            with contextlib.redirect_stderr(captured_output):
                with containers.Tk() as tk:
                    tk.at_exit(callback_raise, ensure_destroy=False)
                    tk.call(tk.wm_protocol("WM_DELETE_WINDOW"))

            self.assertTrue(bool(captured_output.getvalue()))

    def test_zoom(self) -> None:
        with containers.Tk() as tk:
            with containers.Canvas(tk):
                tk.ratios  # trigger caching
                tk.geometry(size=(23, 33))
                tk.update_idletasks()
                tk._zoom()

    @unittest.mock.patch("tkintertools.core.containers.Tk.theme")
    def test_wrap_method(self, mock_theme: unittest.mock.Mock) -> None:
        with containers.Tk() as tk:
            tk._wrap_method("wm_resizable")
            tk.wm_resizable(False, False)
            mock_theme.assert_called()


class TestToplevel(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = containers.Tk()

    def tearDown(self) -> None:
        self.tk.destroy()

    def test_init(self) -> None:
        self.tl = containers.Toplevel(grab=True, focus=True)


class TestCanvas(unittest.TestCase):

    def test_init(self) -> None:
        with containers.Tk() as tk:
            containers.Canvas(tk, auto_update=True)

    def test_ratios(self) -> None:
        with containers.Tk() as tk:
            with containers.Canvas(tk) as cv:
                cv.place(width=100, height=100)
                cv.update_idletasks()
                self.assertEqual(cv.ratios, (1., 1.))
                cv.place(width=50, height=50)
                cv.update_idletasks()
                self.assertEqual(cv.ratios, (0.5, 0.5))

    def test_theme(self) -> None:
        with containers.Tk() as tk:
            with containers.Canvas(tk) as cv:
                widgets.Button(cv, (0, 0), auto_update=True)
                widgets.Button(cv, (0, 0), auto_update=False)
                widgets.Button(cv, (0, 0), auto_update=True).disable()
                with containers.Canvas(cv):
                    cv.theme(True)

    def test_initialization(self) -> None:
        with containers.Tk() as tk:
            for anchor in "nw", "n", "w", "ne", "sw", "e", "s", "se", "center":
                with containers.Canvas(tk) as cv:
                    cv.place(width=100, height=100, anchor=anchor)
                    cv._initialization()


if __name__ == "__main__":
    unittest.main()
