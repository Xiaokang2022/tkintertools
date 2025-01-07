# pylint: disable=all

import importlib
import platform
import unittest
import unittest.mock

from tkintertools.core import configs, containers
from tkintertools.theme import manager


@unittest.skipIf(platform.system() == "Linux", "No display name.")
class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.tk = containers.Tk()

    def tearDown(self) -> None:
        self.tk.destroy()

    def test_set_and_get_color_mode(self) -> None:
        manager.set_color_mode("light")
        self.assertEqual(manager.get_color_mode(), "light")
        manager.set_color_mode("dark")
        self.assertEqual(manager.get_color_mode(), "dark")

    def test_callback(self) -> None:
        configs.Env.is_dark = False

        manager._callback("Dark")
        self.assertTrue(configs.Env.is_dark)

        manager._callback(":)")
        self.assertFalse(configs.Env.is_dark)

    def test_process_event(self) -> None:
        a = None

        def callback(value: bool) -> None:
            nonlocal a
            a = value

        manager.register_event(callback)

        self.assertTrue(manager._process_event(True))

        manager._process_event(True)
        self.assertTrue(a)
        manager._process_event(False)
        self.assertFalse(a)

        manager.remove_event(callback)
        manager.register_event(lambda: None)

        self.assertFalse(manager._process_event(True))

    @unittest.skipUnless(platform.system() == "Windows", "Only works on Windows OS.")
    def test_apply_theme(self) -> None:
        manager.apply_theme(self.tk, theme="normal")

    @unittest.skipUnless(platform.system() == "Windows", "Only works on Windows OS.")
    def test_apply_file_dnd(self) -> None:
        manager.apply_file_dnd(self.tk, command=lambda _: None)

    @unittest.skipUnless(platform.system() == "Windows", "Only works on Windows OS.")
    def test_customize_window(self) -> None:
        manager.customize_window(self.tk, border_color="red", header_color="green", title_color="blue")

        for border_type in "rectangular", "smallround", "round":
            manager.customize_window(self.tk, border_type=border_type)

        for hide_button in "maxmin", "all", "none":
            manager.customize_window(self.tk, hide_button=hide_button)

        manager.customize_window(self.tk, hide_title_bar=True, disable_maximize_button=True, disable_minimize_button=True)
        manager.customize_window(self.tk, hide_title_bar=False, disable_maximize_button=False, disable_minimize_button=False)

    @unittest.skipUnless(platform.system() == "Windows", "Only works on Windows OS.")
    def test_no_dependencies(self) -> None:
        with unittest.mock.patch.dict("sys.modules", {'darkdetect': None, "pywinstyles": None, "hPyT": None, "win32material": None}):
            importlib.reload(manager)

        self.assertWarns(UserWarning, manager.apply_theme, self.tk, theme="normal")
        self.assertWarns(UserWarning, manager.apply_file_dnd, self.tk, command=lambda _: None)
        self.assertWarns(UserWarning, manager.customize_window, self.tk, header_color="red")
        self.assertWarns(UserWarning, manager.customize_window, self.tk, hide_button="all")
        self.assertWarns(UserWarning, manager.customize_window, self.tk, border_type="round")

        importlib.reload(manager)

    @unittest.skipUnless(platform.system() == "Windows", "Only works on Windows OS.")
    def test_apply_theme_on_Windows10(self) -> None:
        with unittest.mock.patch("platform.win32_ver", return_value=('10', '10.0.19041', 'multiprocessor Free')):
            manager.apply_theme(self.tk, theme="normal")


if __name__ == "_-main__":
    unittest.main
