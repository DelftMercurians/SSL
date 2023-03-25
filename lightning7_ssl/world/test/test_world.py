import unittest
from lightning7_ssl.world.world import UninitializedError, World
from lightning7_ssl.control_client.protobuf.ssl_detection_pb2 import SSL_DetectionFrame
from lightning7_ssl.vecMath.vec_math import Vec3, Vec2
from lightning7_ssl.world import BallData, RobotData


class FrameGenerator:
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
    """Generates synthetic estimations."""

    def __init__(self):
        self.own_team = [None, None, None, None, None, None]
        self.opp_team = [None, None, None, None, None, None]
        self.ball_status = None

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
    def test_unitialized_states(self):
        # get_*_state() should return None if the state is not initialized.
        world = World()
        self.assertIsNone(world.get_ball_state())
        self.assertIsNone(world.get_team_state())
        self.assertIsNone(world.get_opp_state())

    def test_uninitialized_accessors(self):
        # get_*_<property>() should raise an UninitializedError if the state is not initialized.
        world = World()
        with self.assertRaises(UninitializedError):
            world.get_team_position()
        with self.assertRaises(UninitializedError):
            world.get_opp_position()
        with self.assertRaises(UninitializedError):
            world.get_robot_pos(0)
        with self.assertRaises(UninitializedError):
            world.get_robot_vel(0)

    def test_getter(self):
        # get_*_<property>() should return the correct value.
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
        # test a complex scenario
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
        world.update_vision_data(frame.get_frame())

        # initial check
        self.assertEqual(world.get_ball_state(), expected.ball_status)
        self.assertEqual(world.get_team_state(), expected.own_team)
        self.assertEqual(world.get_opp_state(), expected.opp_team)

        # move ball
        frame = FrameGenerator()
        frame.add_ball(2.0, 2.0, 2.0, 1.0)
        frame.set_time(2.0)
        expected.update_ball(Vec3(2.0, 2.0, 2.0), Vec3(1, 1, 1))
        world.update_vision_data(frame.get_frame())
        self.assertEqual(world.get_ball_state(), expected.ball_status)

        # move one robot
        frame = FrameGenerator()
        frame.add_robot(0, 2.0, 2.0, 1, False)
        frame.set_time(4.0)
        expected.update_robot(0, Vec2(2.0, 2.0), 1.0, Vec2(0.25, 0.5), 0.25, False)
        world.update_vision_data(frame.get_frame())
        self.assertEqual(world.get_team_state(), expected.own_team)


if __name__ == "__main__":
    unittest.main()
