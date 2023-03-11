import unittest
from lightning7_ssl.player.pathfinder import get_relative_speed
from lightning7_ssl.vecMath.vec_math import Vec2


class MyTestCase(unittest.TestCase):
    def test(self):
        pos1 = Vec2(0, 0)
        pos2 = Vec2(3, 4)
        speed1 = Vec2(1, 2)
        speed2 = Vec2(2, 1)
        expected = 0.2
        result = get_relative_speed(pos1, pos2, speed1, speed2)
        self.assertAlmostEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
