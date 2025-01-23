# pylint: disable=all

import contextlib
import io
import platform
import tkinter
import unittest
import unittest.mock

from maliang.core import containers
from maliang.standard import widgets
from maliang.toolbox import enhanced


class TestTk(unittest.TestCase):

    def test_init(self) -> None:
        containers.Tk(icon="").destroy()
        containers.Tk(title=":)").destroy()

    def test_ratios(self) -> None:
        with containers.Tk() as tk:
            self.assertEqual(tk.ratios, (1., 1.))
            tk.wm_geometry(f"{tk.size[0]//2}x{tk.size[1]//2}")
            tk.update()
            tk._zoom()
            self.assertEqual(tk.ratios, (0.5, 0.5))

    def test_icon(self) -> None:
        with containers.Tk() as tk:
            if platform.system() != "Linux":
                tk.icon("")
                tk.icon("tests/assets/images/logo.ico")

            tk.icon(enhanced.PhotoImage(file="tests/assets/images/logo.png", master=tk))

    def test_alpha(self) -> None:
        with containers.Tk() as tk:
            self.assertEqual(tk.alpha(), 1.)
            self.assertIsNone(tk.alpha(0.8))
            self.assertEqual(tk.alpha(), 0.8)

    def test_topmost(self) -> None:
        with containers.Tk() as tk:
            self.assertIsNone(tk.topmost())
            tk.after(1, lambda: self.assertTrue(tk.topmost(None)))  # Linux needs a short pause
            tk.update()
            self.assertIsNone(tk.topmost(False))
            self.assertFalse(tk.topmost(None))

    # TODO: Test on Darwin and  Linux
    @unittest.skipUnless(platform.system() == "Windows", "The results are difficult to test")
    def test_fullscreen(self) -> None:
        with containers.Tk() as tk:
            self.assertIsNone(tk.fullscreen())
            self.assertTrue(tk.fullscreen(None))
            self.assertIsNone(tk.fullscreen(False))
            self.assertFalse(tk.fullscreen(None))

    @unittest.skipUnless(platform.system() == "Windows", "Only works on Windows")
    def test_toolwindow(self) -> None:
        with containers.Tk() as tk:
            self.assertIsNone(tk.toolwindow())
            self.assertTrue(tk.toolwindow(None))
            self.assertIsNone(tk.toolwindow(False))
            self.assertFalse(tk.toolwindow(None))

    @unittest.skipUnless(platform.system() == "Windows", "Only works on Windows")
    def test_transparentcolor(self) -> None:
        with containers.Tk() as tk:
            self.assertEqual(tk.transparentcolor(), None)
            self.assertIsNone(tk.transparentcolor("red"))
            self.assertEqual(str(tk.transparentcolor()), "red")
            self.assertIsNone(tk.transparentcolor(""))
            self.assertEqual(tk.transparentcolor(), None)

    @unittest.skipUnless(platform.system() == "Darwin", "Only works on Darwin")
    def test_modified(self) -> None:
        with containers.Tk() as tk:
            self.assertFalse(tk.modified())
            self.assertIsNone(tk.modified(True))
            self.assertTrue(tk.modified())

    @unittest.skipUnless(platform.system() == "Darwin", "Only works on Darwin")
    def test_transparent(self) -> None:
        with containers.Tk() as tk:
            self.assertFalse(tk.transparent())
            self.assertIsNone(tk.transparent(True))
            self.assertTrue(tk.transparent())

    def test_center(self) -> None:
        with containers.Tk() as tk:
            tk.center()
            with containers.Toplevel() as tl:
                tl.center(refer=tk)

    def test_theme(self) -> None:
        with containers.Tk() as tk:
            with containers.Toplevel(tk):
                with containers.Canvas(tk):
                    tk.theme("dark", include_children=True, include_canvases=True)

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
                tk.update()
                tk._zoom()

    @unittest.mock.patch("maliang.core.containers.Tk.theme")
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
                cv.update()
                self.assertEqual(cv.ratios, (1., 1.))
                cv.place(width=50, height=50)
                cv.update()
                self.assertEqual(cv.ratios, (0.5, 0.5))

    def test_theme(self) -> None:
        with containers.Tk() as tk:
            with containers.Canvas(tk) as cv:
                widgets.Button(cv, (0, 0), auto_update=True)
                widgets.Button(cv, (0, 0), auto_update=False)
                widgets.Button(cv, (0, 0), auto_update=True).disable()
                with containers.Canvas(cv):
                    cv.theme("dark")

    def test_initialization(self) -> None:
        with containers.Tk() as tk:
            for anchor in "nw", "n", "w", "ne", "sw", "e", "s", "se", "center":
                with containers.Canvas(tk) as cv:
                    cv.place(width=100, height=100, anchor=anchor)
                    cv._initialization()

    def test_zoom_tk_widgets(self) -> None:
        with containers.Tk() as tk:
            with containers.Canvas(tk) as cv:
                tkinter.Button(cv).place(x=0, y=0)
                with containers.Canvas(cv):
                    cv._zoom_tk_widgets(rel_ratio=(1., 1.))

    def test_clear(self) -> None:
        with containers.Tk() as tk:
            with containers.Canvas(tk) as cv:
                tkinter.Button(cv)
                cv.clear()

    def test_zoom_self(self) -> None:
        with containers.Tk() as tk:
            with containers.Canvas(tk, auto_zoom=True, zoom_all_items=True) as cv:
                containers.Canvas(cv)
                widgets.Button(cv, (0, 0))
                cv.create_rectangle(0, 0, 1, 1)
                cv.place(width=100, height=100)
                cv._initialization()
                cv._zoom_self()

    def test_create_text(self) -> None:
        with containers.Tk() as tk:
            with containers.Canvas(tk) as cv:
                cv.create_text(0, 0)
                cv.create_text(0, 0, font=10)
                cv.create_text(0, 0, font="Aria")
                cv.create_text(0, 0, font=("Aria", 10, "bold"))

    def test_zoom(self) -> None:
        with containers.Tk() as tk:
            with containers.Canvas(tk, free_anchor=True) as cv:
                with unittest.mock.patch("maliang.core.containers.Canvas.winfo_viewable", return_value=True):
                    cv.place(width=100, height=100)
                    cv._initialization()
                    cv.zoom()

    def test_on_events(self) -> None:
        with containers.Tk() as tk:
            with containers.Canvas(tk) as cv:
                widgets.Button(cv, (0, 0), capture_events=True)
                widgets.Button(cv, (0, 0))
                event = tkinter.Event()
                event.x = 1
                event.y = 1
                event.char = ":)"
                cv.on_motion(event, "<Motion>")
                event.x = 1
                cv.on_click(event, "<Button-1>")
                event.x = 1
                cv.on_release(event, "<ButtonRelease-1>")
                event.x = 1
                cv.on_wheel(event, True)
                event.x = 1
                cv.on_key_press(event)
                event.x = 1
                cv.on_key_release(event)

    def test_register_event(self) -> None:
        with containers.Tk() as tk:
            with containers.Canvas(tk) as cv:
                widget = widgets.Button(cv, (0, 0))
                cv.register_event("<<Test>>")
                widget.bind("<<Test>>", lambda _: True)
                cv.event_generate("<<Test>>")


if __name__ == "__main__":
    unittest.main()
