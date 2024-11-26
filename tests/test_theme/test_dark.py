# pylint: disable=all

import unittest

from tkintertools.standard import images, shapes, texts, widgets
from tkintertools.theme import dark


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.no_name_widgets = {"Image", "SpinBox"}
        self.component_names = shapes.__all__ + texts.__all__ + images.__all__

    def test_widget_name(self) -> None:
        for widget in set(widgets.__all__) - self.no_name_widgets:
            self.assertIsNotNone(getattr(dark, widget, None), widget)

    def test_component_name(self) -> None:
        for widget in set(widgets.__all__) - self.no_name_widgets:
            for component_name in getattr(dark, widget):
                self.assertIn(component_name.split(".")[0], self.component_names, component_name)


if __name__ == "__main__":
    unittest.main()
