# pylint: disable=all

import contextlib
import importlib
import io
import platform
import unittest
import unittest.mock

from maliang.core import configs, containers
from maliang.theme import manager


class TestCase(unittest.TestCase):

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
        configs.Env.theme = "light"

        manager._callback("Dark")
        self.assertEqual(configs.Env.theme, "dark")

        manager._callback(":)")
        self.assertEqual(configs.Env.theme, "light")

    def test_process_event(self) -> None:
        a = None

        def callback(value: bool) -> None:
            nonlocal a
            a = value

        manager.register_event(callback)

        manager._process_event("dark")
        self.assertEqual(a, "dark")
        manager._process_event("light")
        self.assertEqual(a, "light")

        manager.remove_event(callback)
        manager.register_event(f := lambda: None)

        with io.StringIO() as captured_output:
            with contextlib.redirect_stderr(captured_output):
                manager._process_event("dark")

            self.assertTrue(bool(captured_output.getvalue()))

        manager.remove_event(f)

    @unittest.skipUnless(platform.system() == "Windows", "Only works on Windows OS.")
    def test_apply_theme(self) -> None:
        manager.apply_theme(self.tk, theme="normal")
        manager.apply_theme(self.tk, theme="mica")
        manager.apply_theme(self.tk, theme="acrylic2")

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
        self.assertWarns(UserWarning, manager.apply_theme, self.tk, theme="mica")
        self.assertWarns(UserWarning, manager.apply_file_dnd, self.tk, command=lambda _: None)
        self.assertWarns(UserWarning, manager.customize_window, self.tk, header_color="red")
        self.assertWarns(UserWarning, manager.customize_window, self.tk, hide_button="all")
        self.assertWarns(UserWarning, manager.customize_window, self.tk, border_type="round")

        importlib.reload(manager)

    @unittest.skipUnless(platform.system() == "Windows", "Only works on Windows OS.")
    def test_apply_theme_on_Windows10(self) -> None:
        with unittest.mock.patch("platform.win32_ver", return_value=('10', '10.0.19041', 'multiprocessor Free')):
            manager.apply_theme(self.tk, theme="normal")


if __name__ == "__main__":
    unittest.main()
