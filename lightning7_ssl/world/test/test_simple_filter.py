import unittest
from lightning7_ssl.world.common import *
from lightning7_ssl.world.simple_filter import SimpleFilter
import math


class MyTestCase(unittest.TestCase):
    def test_ball_filter(self):
        filter = SimpleFilter()
        records = OrderedDict()
        # test empty
        self.assertIsNone(filter.ball_filter(records))
        # test avg
        records[0] = [
            BallDataRaw(0, 0, (0, 0, 0), 0.3),
            BallDataRaw(0, 1, (0.1, 0.1, 0), 0.5),
            BallDataRaw(0, 2, (0.2, 0.2, 0), 0.7),
        ]
        res = filter.ball_filter(records)
        self.assertEqual(res, BallDataEstimated((0.2, 0.2, 0), (0, 0, 0)))
        # test speed
        records[0.5] = [BallDataRaw(0.5, 2, (1.1, 1.1, 1), 1)]
        records[1] = [BallDataRaw(1, 2, (1.9, 1.4, 0), 1)]
        speed = filter.ball_filter(records).velocity
        self.assertTrue(math.isclose(speed[0], 1.6))
        self.assertTrue(math.isclose(speed[1], 0.6))
        self.assertTrue(math.isclose(speed[2], -2))

    def test_robot_filter(self):
        filter = SimpleFilter()
        records = OrderedDict()
        # test empty
        self.assertIsNone(filter.robot_filter(records))
        # test avg
        records[0] = [
            RobotDataRaw(0, 0, (0, 0), 0.0),
            RobotDataRaw(0, 1, (0.1, 0.1), 0.5),
            RobotDataRaw(0, 2, (0.5, 0.2), 0.7),
        ]
        res = filter.robot_filter(records)
        self.assertTrue(math.isclose(res.position[0], 0.2))
        self.assertTrue(math.isclose(res.position[1], 0.1))
        self.assertTrue(math.isclose(res.orientation, 0.4))
        # test speed
        records[0.5] = [RobotDataRaw(0.5, 2, (1.1, 1.1), 1)]
        records[1] = [RobotDataRaw(1, 2, (1.9, 1.4), 1.7)]
        res = filter.robot_filter(records)
        speed = res.velocity
        spin = res.angular_speed
        self.assertTrue(math.isclose(speed[0], 1.6))
        self.assertTrue(math.isclose(speed[1], 0.6))
        self.assertTrue(math.isclose(spin, 1.4))


if __name__ == "__main__":
    unittest.main()
