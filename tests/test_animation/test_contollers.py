# pylint: disable=all

import math
import unittest

from maliang.animation import controllers


class TestCase(unittest.TestCase):

    def test_linear(self) -> None:
        self.assertEqual(controllers.linear(0), 0)
        self.assertEqual(controllers.linear(0.618), 0.618)
        self.assertEqual(controllers.linear(1), 1)

    def test_smooth(self) -> None:
        self.assertEqual(controllers.smooth(0), 0)
        self.assertEqual(controllers.smooth(1), 1)
        self.assertAlmostEqual(controllers.smooth(1/4), 1/2 - math.sqrt(2)/4)
        self.assertAlmostEqual(controllers.smooth(2/4), 1/2)
        self.assertAlmostEqual(controllers.smooth(3/4), 1/2 + math.sqrt(2)/4)

    def test_rebound(self) -> None:
        self.assertEqual(controllers.rebound(0), 0)
        self.assertEqual(controllers.rebound(1), 1)
        self.assertAlmostEqual(controllers.rebound(1/4), 0.5639150830548166)
        self.assertAlmostEqual(controllers.rebound(2/4), 0.9800394839160321)
        self.assertAlmostEqual(controllers.rebound(3/4), 1.1393154544781496)

    def test_ease_in(self) -> None:
        self.assertAlmostEqual(controllers.ease_in(0), 0, 2)
        self.assertEqual(controllers.ease_in(1), 1)
        self.assertAlmostEqual(controllers.ease_in(0.75), 0.176776, 2)

    def test_ease_out(self) -> None:
        self.assertEqual(controllers.ease_out(0), 0)
        self.assertEqual(controllers.ease_out(1), 1)
        self.assertAlmostEqual(controllers.ease_out(0.25), 1-0.176776, 2)

    def test_generate(self) -> None:
        func_1 = controllers.generate(lambda x: x, 233, 666, map_y=False)
        self.assertEqual(func_1(0), 233)
        self.assertEqual(func_1(1), 666)

        func_2 = controllers.generate(math.sin, 0, math.pi, map_y=False)
        self.assertAlmostEqual(func_2(0), 0)
        self.assertAlmostEqual(func_2(1), 0)
        self.assertAlmostEqual(func_2(1/2), 1)
        self.assertAlmostEqual(func_2(2), 0)

        func_3 = controllers.generate(lambda x: x, 233, 666)
        self.assertAlmostEqual(func_3(0), 233/666)
        self.assertAlmostEqual(func_3(0.618), (233 + 0.618*(666-233)) / 666)
        self.assertAlmostEqual(func_3(1), 1)

        self.assertWarns(UserWarning, controllers.generate, math.sin, math.pi, math.tau)


if __name__ == "__main__":
    unittest.main()
