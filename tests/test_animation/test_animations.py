# pylint: disable=all

import platform
import tkinter
import unittest

from tkintertools.animation import animations, controllers
from tkintertools.core import containers
from tkintertools.standard import widgets


class TestAnimation(unittest.TestCase):

    def setUp(self):
        self.tk = tkinter.Tk()

    def tearDown(self):
        self.tk.destroy()

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test_fps(self) -> None:
        an = animations.Animation(60, lambda _: None, fps=100)
        an2 = animations.Animation(60, lambda _: None, fps=50)
        an3 = animations.Animation(1, lambda _: None)

        an.start()
        self.assertEqual(len(an._tasks), 6+1)
        an2.start()
        self.assertEqual(len(an2._tasks), 3+1)
        an3.start()
        self.assertEqual(len(an3._tasks), 1+1)

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test_active(self) -> None:
        an = animations.Animation(60, lambda _: None)
        an.start()
        self.assertEqual(an.active, True)
        an.stop()
        self.assertEqual(an.active, False)

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test_count(self) -> None:
        an = animations.Animation(60, lambda _: None)
        an2 = animations.Animation(60, lambda _: None, repeat=2)

        an.start()
        self.assertEqual(an.count, 0)
        an.stop()
        self.assertEqual(an.count, 0)

        an2.start()
        self.assertEqual(an2.count, 2)
        an2.stop()
        self.assertEqual(an2.count, 2)

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test_total_frames(self) -> None:
        an = animations.Animation(60, lambda _: None, fps=1)
        self.assertEqual(an._delay, 60)
        self.assertEqual(an._total_frames, 1)
        self.assertEqual(an._leave_ms, 0)

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test_repeat(self) -> None:
        an = animations.Animation(60, lambda _: None, repeat=0)
        an2 = animations.Animation(60, lambda _: None, repeat=1)
        an3 = animations.Animation(60, lambda _: None, repeat=2)
        an4 = animations.Animation(60, lambda _: None, repeat=2, repeat_delay=1)
        an._repeat()
        an2._repeat()
        an3._repeat()
        an4._repeat()

        self.assertEqual(an.count, 0)
        self.assertEqual(len(an._tasks), 0)
        self.assertEqual(an2.count, 0)
        self.assertEqual(len(an2._tasks), 2)
        self.assertEqual(an3.count, 1)
        self.assertEqual(len(an3._tasks), 2)
        self.assertEqual(an4.count, 1)
        self.assertEqual(len(an4._tasks), 1)

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test_delay(self) -> None:
        an1 = animations.Animation(60, lambda _: None, repeat=1)
        a = an1.start(delay=0)
        b = an1.stop(delay=0)
        an2 = animations.Animation(60, lambda _: None, repeat=1)
        c = an2.start(delay=1)
        d = an2.stop(delay=1)
        self.assertIsNone(a)
        self.assertIsNone(b)
        self.assertIsInstance(c, str)
        self.assertIsInstance(d, str)

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test_end(self) -> None:
        an = animations.Animation(60, lambda _: None, fps=50, end=lambda: None)
        an.start()
        self.assertEqual(len(an._tasks), 3+2)


class TestMoveWindow_Tk(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = tkinter.Tk()
        self.tk.geometry("+100+100")
        self.top = tkinter.Toplevel(self.tk)
        self.top.geometry("+100+100")

    def tearDown(self) -> None:
        self.tk.destroy()

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test(self) -> None:
        animations.MoveWindow(self.tk, (99, 99), 1, fps=1).callback(1)
        animations.MoveWindow(self.top, (99, 99), 1, fps=1).callback(1)

        self.tk.update_idletasks()
        self.top.update_idletasks()

        self.assertEqual(self.tk.winfo_x(), 199)
        self.assertEqual(self.top.winfo_y(), 199)


class TestMoveWindow(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = containers.Tk(position=(200, 200))
        self.top = containers.Toplevel(self.tk, position=(200, 200))

    def tearDown(self) -> None:
        self.tk.destroy()

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test(self) -> None:
        animations.MoveWindow(self.tk, (-99, -99), 1, fps=1).callback(1)
        animations.MoveWindow(self.top, (-99, -99), 1, fps=1).callback(1)

        self.tk.update_idletasks()
        self.top.update_idletasks()

        self.assertEqual(self.tk.winfo_x(), 101)
        self.assertEqual(self.top.winfo_y(), 101)


class TestMoveTkWidget(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = tkinter.Tk()
        self.widget = tkinter.Label(self.tk)
        self.widget2 = tkinter.Label(self.tk)
        self.widget2.pack()
        self.widget3 = tkinter.Label(self.tk)
        self.widget3.place(x=10, y=10)

    def tearDown(self) -> None:
        self.tk.destroy()

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test(self) -> None:
        self.assertWarns(UserWarning, lambda: animations.MoveTkWidget(self.widget, (99, 99), 99))
        self.assertWarns(UserWarning, lambda: animations.MoveTkWidget(self.widget2, (99, 99), 99))
        animations.MoveTkWidget(self.widget3, (99, 99), 99).start()


class TestMoveWidget(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = containers.Tk()
        self.cv = containers.Canvas(self.tk)
        self.widget = widgets.Button(self.cv, (10, 10))

    def tearDown(self) -> None:
        self.tk.destroy()

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test(self) -> None:
        animations.MoveWidget(self.widget, (99, 99), 99).start()


class TestMoveComponent(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = containers.Tk()
        self.cv = containers.Canvas(self.tk)
        self.widget = widgets.Button(self.cv, (10, 10))

    def tearDown(self) -> None:
        self.tk.destroy()

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test(self) -> None:
        animations.MoveComponent(self.widget.components[0], (99, 99), 99).start()


class TestMoveItem(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = containers.Tk()
        self.cv = containers.Canvas(self.tk)
        self.item = self.cv.create_rectangle(10, 10, 20, 20)

    def tearDown(self) -> None:
        self.tk.destroy()

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test(self) -> None:
        animations.MoveItem(self.cv, self.item, (99, 99), 99).start()


class TestGradientTkWidget(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = tkinter.Tk()
        self.widget = tkinter.Label(self.tk)

    def tearDown(self) -> None:
        self.tk.destroy()

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test(self) -> None:
        animations.GradientTkWidget(self.widget, "fill", ("red", "#00FF00"), 99).start()
        self.assertRaises(ValueError, lambda: animations.GradientTkWidget(self.widget, "fill", ("", ""), 1000))


class TestGradientItem(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = tkinter.Tk()
        self.cv = tkinter.Canvas(self.tk)
        self.item = self.cv.create_rectangle(10, 10, 20, 20)

    def tearDown(self) -> None:
        self.tk.destroy()

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test(self) -> None:
        animations.GradientItem(self.cv, self.item, "fill", ("red", "#0000FF"), 99).start()
        self.assertRaises(ValueError, lambda: animations.GradientItem(self.cv, self.item, "fill", ("", ""), 1000))


class TestScaleFontSize(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = containers.Tk()
        self.cv = containers.Canvas(self.tk)
        self.widget = widgets.Text(self.cv, (10, 10), text="Hello, World!")

    def tearDown(self) -> None:
        self.tk.destroy()

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test(self) -> None:
        animations.ScaleFontSize(self.widget.texts[0], 10, 99).start()
        animations.ScaleFontSize(self.widget.texts[0], 24.5, 99).start()
        animations.ScaleFontSize(self.widget.texts[0], (10, 20), 99).start()
        animations.ScaleFontSize(self.widget.texts[0], (11.1, 22.2), 99).start()


if __name__ == "__main__":
    unittest.main()
