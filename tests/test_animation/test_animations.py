# pylint: disable=all

import platform
import tkinter
import unittest

from tkintertools.animation import animations, controllers


class TestAnimation_NoTk(unittest.TestCase):

    def test_start(self) -> None:
        self.assertRaises(AttributeError, animations.Animation(1000, controllers.flat).start)


class TestAnimation(unittest.TestCase):

    def setUp(self):
        self.tk = tkinter.Tk()

    def tearDown(self):
        self.tk.destroy()

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test_fps(self) -> None:
        an = animations.Animation(60, controllers.flat, fps=100)
        an2 = animations.Animation(60, controllers.flat, fps=50)
        an3 = animations.Animation(1, controllers.flat)

        an.start()
        self.assertEqual(len(an._tasks), 6)
        an2.start()
        self.assertEqual(len(an2._tasks), 3)
        an3.start()
        self.assertEqual(len(an3._tasks), 1)

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test_is_active(self) -> None:
        an = animations.Animation(60, controllers.flat)
        an.start()
        self.assertEqual(an.is_active, True)
        an.stop()
        self.assertEqual(an.is_active, False)


class TestMoveTkWidget(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = tkinter.Tk()
        self.widget = tkinter.Label(self.tk)

    def tearDown(self) -> None:
        self.tk.destroy()

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test(self) -> None:
        self.assertWarns(
            UserWarning, lambda: animations.MoveTkWidget(self.widget, 1000, (100, 100)))


class TestGradientTkWidget(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = tkinter.Tk()
        self.widget = tkinter.Label(self.tk)

    def tearDown(self) -> None:
        self.tk.destroy()

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test(self) -> None:
        self.assertRaises(
            ValueError, lambda: animations.GradientTkWidget(self.widget, "fill", 1000, ("", "")))


class TestGradientItem(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.tk)

    def tearDown(self) -> None:
        self.tk.destroy()

    @unittest.skipIf(platform.system() == "Linux", "No display name.")
    def test(self) -> None:
        self.assertRaises(
            ValueError, lambda: animations.GradientItem(self.canvas, 0, "fill", 1000, ("", "")))


if __name__ == "__main__":
    unittest.main()
