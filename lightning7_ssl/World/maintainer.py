from typing import List
import numpy as np
from dataclasses import dataclass
from common import *
from simple_filter import SimpleFilter
from lightning7_ssl.control_client.protobuf.ssl_simulation_robot_control_pb2 import RobotControl
from lightning7_ssl.control_client.protobuf.ssl_wrapper_pb2 import SSL_WrapperPacket

@dataclass
class filteredDataWrapper:
    ball_status: BallDataEstimated
    own_robots_status: List[RobotDataEstimated]
    opp_robots_status: List[RobotDataEstimated]

    def __str__(self):
        pass


class World:
    """Represents the current state of the world."""
    def __init__(self, num_robots = 7, is_blue = True):
        filter = SimpleFilter()
        self.own_robots_status = []
        self.opp_robots_status = []
        self.ball_status = BallTracker(filter)
        self.is_blue = is_blue
        self.num_robots = num_robots
        for i in range(num_robots):
            self.own_robots_status.append(RobotTracker(filter))
            self.opp_robots_status.append(RobotTracker(filter))

    @staticmethod
    def get_status(self) -> filteredDataWrapper:
        """Returns the current world state."""
        return filteredDataWrapper(self.ball_status.get(), [tracker.get() for tracker in self.own_robots_status],
                                   [tracker.get() for tracker in self.opp_robots_status])

    @staticmethod
    def update_vision_data(self, data: bytes):
        """Updates the world state from vision data."""
        packet = SSL_WrapperPacket()
        packet.ParseFromString(data)
        frame = packet.detection
        camera_id = frame.camera_id
        time = frame.t_capture
        if frame is None:
            return None, None, None
        for ball in frame.balls:
            self.ball_status.add(BallDataRaw(time,camera_id,Vector3(ball.x, ball.y, ball.z), ball.confidence))
        for robot in frame.robots_yellow:
            if robot.robot_id < 0 or robot.robot_id >= self.num_robots:
                continue
            if self.is_blue:
                self.opp_robots_status[robot.robot_id].add(RobotDataRaw(time,camera_id,Vector2(robot.x, robot.y), robot.orientation))
            else:
                self.own_robots_status[robot.robot_id].add(RobotDataRaw(time,camera_id,Vector2(robot.x, robot.y), robot.orientation))
        for robot in frame.robots_blue:
            if robot.robot_id < 0 or robot.robot_id >= self.num_robots:
                continue
            if self.is_blue:
                self.own_robots_status[robot.robot_id].add(RobotDataRaw(time,camera_id,Vector2(robot.x, robot.y), robot.orientation))
            else:
                self.opp_robots_status[robot.robot_id].add(RobotDataRaw(time,camera_id,Vector2(robot.x, robot.y), robot.orientation))
        return self.getStatus()


