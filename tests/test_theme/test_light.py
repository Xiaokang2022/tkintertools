# pylint: disable=all

import unittest

from tkintertools.standard import images, shapes, texts, widgets
from tkintertools.theme import light


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.no_name_widgets = {"Image", "SpinBox", "ComboBox"}
        self.element_names = shapes.__all__ + texts.__all__ + images.__all__

    def test_widget_name(self) -> None:
        for widget in set(widgets.__all__) - self.no_name_widgets:
            self.assertIsNotNone(getattr(light, widget, None), widget)

    def test_element_name(self) -> None:
        for widget in set(widgets.__all__) - self.no_name_widgets:
            for element_name in getattr(light, widget):
                self.assertIn(element_name.split(".")[0], self.element_names, element_name)


if __name__ == "__main__":
    unittest.main()
