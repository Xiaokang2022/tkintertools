# pylint: disable=all

import math
import unittest

from tkintertools.animation import controllers


class Test(unittest.TestCase):

    def test_flat(self) -> None:
        self.assertEqual(controllers.flat(0), 0)
        self.assertEqual(controllers.flat(0.618), 0.618)
        self.assertEqual(controllers.flat(1), 1)

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

    def test_controller_generator(self) -> None:
        func_1 = controllers.controller_generator(lambda x: x, 233, 666, map_y=False)
        self.assertEqual(func_1(0), 233)
        self.assertEqual(func_1(1), 666)

        func_2 = controllers.controller_generator(math.sin, 0, math.pi, map_y=False)
        self.assertAlmostEqual(func_2(0), 0)
        self.assertAlmostEqual(func_2(1), 0)
        self.assertAlmostEqual(func_2(1/2), 1)
        self.assertAlmostEqual(func_2(2), 0)

        func_3 = controllers.controller_generator(lambda x: x, 233, 666)
        self.assertAlmostEqual(func_3(0), 233/666)
        self.assertAlmostEqual(func_3(0.618), (233 + 0.618*(666-233)) / 666)
        self.assertAlmostEqual(func_3(1), 1)

        self.assertWarns(UserWarning, controllers.controller_generator, math.sin, math.pi, math.tau)


if __name__ == "__main__":
    unittest.main()
