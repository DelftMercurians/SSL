import unittest
from lightning7_ssl.world.maintainer import World, FilteredDataWrapper
from lightning7_ssl.control_client.protobuf.ssl_detection_pb2 import SSL_DetectionFrame
from lightning7_ssl.world.common import *


class FrameGenerator:
    def __init__(self):
        self.frame = SSL_DetectionFrame()
        self.frame.camera_id = 0
        self.frame.t_capture = 0

    def set_time(self, time):
        self.frame.t_capture = time

    def add_ball(self, x, y, z, confidence):
        ball = self.frame.balls.add()
        ball.x = x
        ball.y = y
        ball.z = z
        ball.confidence = confidence

    def add_robot(self, robot_id, x, y, orientation, is_yellow):
        robot = (
            self.frame.robots_yellow.add()
            if is_yellow
            else self.frame.robots_blue.add()
        )
        robot.robot_id = robot_id
        robot.x = x
        robot.y = y
        robot.orientation = orientation

    def update_robot(self, robot_id, x, y, orientation, is_yellow):
        l = self.frame.robots_yellow if is_yellow else self.frame.robots_blue
        for robot in l:
            if robot.robot_id == robot_id:
                robot.x = x
                robot.y = y
                robot.orientation = orientation
                return

    def get_frame(self):
        return self.frame


class EstimationGenerator:
    def __init__(self):
        own_team = [None, None, None, None, None, None]
        opp_team = [None, None, None, None, None, None]
        ball_status = None
        self.estimation = FilteredDataWrapper(ball_status, own_team, opp_team)

    def update_ball(self, pos: Vec3, speed: Vec3):
        self.estimation.ball_status = BallDataEstimated(pos, speed)

    def update_robot(
        self,
        robot_id,
        pos: Vec2,
        orientation,
        speed: Vec2,
        angular_speed,
        is_yellow,
    ):
        robot = (
            self.estimation.opp_robots_status
            if is_yellow
            else self.estimation.own_robots_status
        )
        robot[robot_id] = RobotDataEstimated(pos, orientation, speed, angular_speed)

    def get_estimation(self):
        return self.estimation


class TestMaintainer(unittest.TestCase):
    def test_empty(self):
        world = World()
        t = str(world.get_status())
        self.assertEqual(t, str(EstimationGenerator().get_estimation()))

    def test_getter(self):
        world = World()
        frame = FrameGenerator()
        expected_own = []
        expected_opp = []
        frame.add_ball(1.0, 1.0, 0, 1.0)
        for i in range(6):
            frame.add_robot(i, -1.0, i, 0, True)  # opp team
            frame.add_robot(i, 1.0, i, 0, False)  # own team
            expected_own.append(Vec2(1.0, float(i)))
            expected_opp.append(Vec2(-1.0, float(i)))
        world.update_vision_data(frame.get_frame())
        self.assertEqual(world.get_team_position(), expected_own)
        self.assertEqual(world.get_opp_position(), expected_opp)
        frame.set_time(1)
        for i in range(6):
            frame.update_robot(i, 0, i, 0, True)
            frame.update_robot(i, 2, i, 0, False)
            expected_own[i] = Vec2(1, 0)
            expected_opp[i] = Vec2(1, 0)
        world.update_vision_data(frame.get_frame())
        self.assertEqual(world.get_team_vel(), expected_own)
        self.assertEqual(world.get_opp_vel(), expected_opp)

    def test_complex(self):
        world = World()
        expected = EstimationGenerator()
        # data preperation
        # init status
        frame = FrameGenerator()
        f = float(0.0)
        frame.add_ball(f, f, f, f)
        expected.update_ball(Vec3(f, f, f), Vec3(f, f, f))
        for i in range(6):
            frame.add_robot(i, -1.0, i, 0, True)  # opp team
            frame.add_robot(i, 1.0, i, 0, False)  # own team
            expected.update_robot(i, Vec2(1.0, float(i)), 0.0, Vec2(f, f), 0.0, False)
            expected.update_robot(i, Vec2(-1.0, float(i)), 0.0, Vec2(f, f), 0.0, True)
        res = world.update_vision_data(frame.get_frame())
        self.assertTrue(res == expected.get_estimation())
        # move ball
        frame = FrameGenerator()
        frame.add_ball(2.0, 2.0, 2.0, 1.0)
        frame.set_time(2.0)
        expected.update_ball(Vec3(2.0, 2.0, 2.0), Vec3(1, 1, 1))
        res = world.update_vision_data(frame.get_frame())
        self.assertTrue(res == expected.get_estimation())
        # move one robot
        frame = FrameGenerator()
        frame.add_robot(0, 2.0, 2.0, 1, False)
        frame.set_time(4.0)
        expected.update_robot(0, Vec2(2.0, 2.0), 1.0, Vec2(0.25, 0.5), 0.25, False)
        res = world.update_vision_data(frame.get_frame())
        self.assertTrue(res == expected.get_estimation())


if __name__ == "__main__":
    unittest.main()
