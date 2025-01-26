# pylint: disable=all

import unittest
import unittest.mock

from maliang.core import configs


class TestEnv(unittest.TestCase):

    def test_reset(self) -> None:
        configs.Env.system = ""
        configs.Env.theme = "dark"
        configs.Env.gradient_animation = False
        configs.Env.auto_update = False

        configs.Env.reset()

        self.assertEqual(configs.Env.system, configs.Env.get_default_system())
        self.assertEqual(configs.Env.theme, "light")
        self.assertTrue(configs.Env.gradient_animation)
        self.assertTrue(configs.Env.auto_update)

    def test_get_default_system(self) -> None:
        with unittest.mock.patch('sys.platform', 'win32'):
            with unittest.mock.patch('platform.win32_ver', return_value=('10', '10.1.22000', 'multiprocessor Free')):
                self.assertEqual(configs.Env.get_default_system(), "Windows11")

        with unittest.mock.patch('sys.platform', 'win32'):
            with unittest.mock.patch('platform.win32_ver', return_value=('10', '10.0.19041', 'multiprocessor Free')):
                self.assertEqual(configs.Env.get_default_system(), "Windows10")

        with unittest.mock.patch('sys.platform', 'linux'):
            with unittest.mock.patch('platform.system', return_value='Linux'):
                self.assertEqual(configs.Env.get_default_system(), "Linux")


class TestFont(unittest.TestCase):

    def test_reset(self) -> None:
        configs.Font.family = ""
        configs.Font.size = 0

        configs.Font.reset()

        self.assertEqual(configs.Font.family, configs.Font.get_default_family())
        self.assertEqual(configs.Font.size, -20)

    def test_get_default_family(self) -> None:
        with unittest.mock.patch('sys.platform', 'win32'):
            self.assertEqual(configs.Font.get_default_family(), "Microsoft YaHei")

        with unittest.mock.patch('sys.platform', 'darwin'):
            self.assertEqual(configs.Font.get_default_family(), "SF Pro")

        with unittest.mock.patch('sys.platform', 'linux'):
            self.assertEqual(configs.Font.get_default_family(), "Noto Sans")


if __name__ == "__main__":
    unittest.main()
