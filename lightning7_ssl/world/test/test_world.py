import unittest
from unittest.mock import Mock

from lightning7_ssl.cfg import GlobalConfig
from lightning7_ssl.control_client.protobuf.ssl_detection_pb2 import SSL_DetectionFrame
from lightning7_ssl.vecMath.vec_math import Vec2, Vec3
from lightning7_ssl.world import BallData, RobotData
from lightning7_ssl.world.world import UninitializedError, World

config = GlobalConfig()


class RawFrameGenerator:
    """Generates synthetic SSL detection frames."""

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
        robot = self.frame.robots_yellow.add() if is_yellow else self.frame.robots_blue.add()
        robot.robot_id = robot_id
        robot.x = x
        robot.y = y
        robot.orientation = orientation

    def update_robot(self, robot_id, x, y, orientation, is_yellow):
        robots = self.frame.robots_yellow if is_yellow else self.frame.robots_blue
        for robot in robots:
            if robot.robot_id == robot_id:
                robot.x = x
                robot.y = y
                robot.orientation = orientation
                return

    def get_frame(self):
        return self.frame


class EstimationGenerator:
    """Generates synthetic estimations."""

    def __init__(self) -> None:
        self.own_team: list[RobotData | None] = [None, None, None, None, None, None]
        self.opp_team: list[RobotData | None] = [None, None, None, None, None, None]
        self.ball_status: BallData | None = None

    def update_ball(self, pos: Vec3, speed: Vec3):
        self.ball_status = BallData(pos, speed)

    def update_robot(
        self,
        robot_id,
        pos: Vec2,
        orientation,
        speed: Vec2,
        angular_speed,
        is_yellow,
    ):
        robot = self.opp_team if is_yellow else self.own_team
        robot[robot_id] = RobotData(pos, orientation, speed, angular_speed)


class WorldTestSuite(unittest.TestCase):
    def test_unitialized_frame(self):
        # frame() should raise an UninitializedError if the state is not initialized.
        world = World(Mock(), config)
        with self.assertRaises(UninitializedError):
            world.frame()

    def test_getter(self):
        # frame() should return the current frame.
        world = World(Mock(), config)
        raw_frame = RawFrameGenerator()
        expected_own = []
        expected_opp = []
        raw_frame.add_ball(1.0, 1.0, 0, 1.0)
        for i in range(6):
            raw_frame.add_robot(i, -1.0, i, 0, True)  # opp team
            raw_frame.add_robot(i, 1.0, i, 0, False)  # own team
            expected_own.append(Vec2(1.0, float(i)))
            expected_opp.append(Vec2(-1.0, float(i)))
        world.update_vision_data(raw_frame.get_frame())
        world.update_vision_data(raw_frame.get_frame())
        world.update_vision_data(raw_frame.get_frame())

        self.assertEqual(world.frame().ball.position, Vec3(1.0, 1.0, 0))
        self.assertEqual(world.frame().ball.velocity, Vec3(0, 0, 0))
        self.assertEqual([p.position for p in world.frame().own_players], expected_own)
        self.assertEqual([p.position for p in world.frame().opp_players], expected_opp)

    def test_complex(self):
        # test a complex scenario
        world = World(Mock(), config)
        expected = EstimationGenerator()
        # data preperation
        # init status
        frame = RawFrameGenerator()
        f = float(0.0)
        frame.add_ball(f, f, f, f)
        expected.update_ball(Vec3(f, f, f), Vec3(f, f, f))
        for i in range(6):
            frame.add_robot(i, -1.0, i, 0, True)  # opp team
            frame.add_robot(i, 1.0, i, 0, False)  # own team
            expected.update_robot(i, Vec2(1.0, float(i)), 0.0, Vec2(f, f), 0.0, False)
            expected.update_robot(i, Vec2(-1.0, float(i)), 0.0, Vec2(f, f), 0.0, True)
        world.update_vision_data(frame.get_frame())
        world.update_vision_data(frame.get_frame())

        # initial check
        self.assertEqual(world.frame().ball.position, Vec3(f, f, f))
        self.assertEqual(world.frame().own_players, expected.own_team)
        self.assertEqual(world.frame().opp_players, expected.opp_team)

        # move ball
        frame = RawFrameGenerator()
        frame.add_ball(2.0, 2.0, 2.0, 1.0)
        frame.set_time(2.0)
        expected.update_ball(Vec3(2.0, 2.0, 2.0), Vec3(1, 1, 1))
        world.update_vision_data(frame.get_frame())
        self.assertEqual(world.frame().ball.position, Vec3(2.0, 2.0, 2.0))

        # move one robot
        frame = RawFrameGenerator()
        frame.add_robot(0, 2.0, 2.0, 1, False)
        frame.set_time(4.0)
        expected.update_robot(0, Vec2(2.0, 2.0), 1.0, Vec2(0.25, 0.5), 0.25, False)
        world.update_vision_data(frame.get_frame())
        self.assertEqual(world.frame().own_players[0].position, Vec2(2.0, 2.0))


if __name__ == "__main__":
    unittest.main()
