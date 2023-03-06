import unittest
from lightning7_ssl.player.pathfinder import get_relative_speed

class MyTestCase(unittest.TestCase):
    def test(self):
        pos1 = (0, 0)
        pos2 = (3, 4)
        speed1 = (1, 2)
        speed2 = (2, 1)
        expected = 0.2
        result = get_relative_speed(pos1, pos2, speed1, speed2)
        self.assertAlmostEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
