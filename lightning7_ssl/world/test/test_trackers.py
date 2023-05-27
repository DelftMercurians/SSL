import unittest

from lightning7_ssl.vecMath.vec_math import Vec2, Vec3
from lightning7_ssl.world.processing import (
    BallDataRaw,
    BallTracker,
    RobotDataRaw,
    RobotTracker,
)
from lightning7_ssl.world.processing.simple_estimator import SimpleEstimator


class TrackersTestSuite(unittest.TestCase):
    camera_id = 0
    time1 = 526.4772159998272
    pos1 = (-3943.85302734375, 1551.4298095703125)
    orientation1 = 0.0
    time2 = 526.4938829998272
    pos2 = (-3937.513427734375, 1553.5130615234375)
    orientation2 = 0.15

    def test_robo_traker(self):
        filter = SimpleEstimator()
        p1 = RobotDataRaw(self.time1, self.camera_id, Vec2(*self.pos1), self.orientation1)
        p1s = RobotDataRaw(self.time1, self.camera_id, Vec2(*self.pos2), self.orientation1)
        p2 = RobotDataRaw(self.time2, self.camera_id, Vec2(*self.pos2), self.orientation2)
        # test creation
        robot_tracker = RobotTracker(filter, 2)
        # test add
        robot_tracker.add(p1)
        robot_tracker.add(p1s)
        self.assertEqual(robot_tracker.record.get(self.time1)[0], p1)  # type: ignore
        self.assertEqual(robot_tracker.record.get(self.time1)[1], p1s)  # type: ignore
        # test overflow
        lastest = RobotDataRaw(self.time2 + self.time1, self.camera_id, Vec2(*self.pos2), self.orientation2)
        robot_tracker.add(p2)
        robot_tracker.add(lastest)
        self.assertFalse(robot_tracker.record.__contains__(self.time1))
        self.assertTrue(robot_tracker.record.__contains__(self.time2))
        self.assertTrue(robot_tracker.record.__contains__(self.time1 + self.time2))

    pos_ball_1 = (0, 0, 0)
    pos_ball_2 = (1, 1, 1)

    def test_ball_tracker(self):
        filter = SimpleEstimator()
        p1 = BallDataRaw(self.time1, self.camera_id, Vec3(*self.pos_ball_1), 1)
        p2 = BallDataRaw(self.time2, self.camera_id, Vec3(*self.pos_ball_2), 1)
        # test creation
        ball_tracker = BallTracker(filter, 2)
        # test add
        ball_tracker.add(p1)
        ball_tracker.add(p2)
        self.assertEqual(ball_tracker.record.get(self.time1), [p1])
        self.assertEqual(ball_tracker.record.get(self.time2), [p2])


if __name__ == "__main__":
    unittest.main()
