from typing import List
import numpy as np
from dataclasses import dataclass
from lightning7_ssl.world.common import *
from lightning7_ssl.world.simple_filter import SimpleFilter
from lightning7_ssl.control_client.protobuf.ssl_detection_pb2 import SSL_DetectionFrame
from lightning7_ssl.control_client.protobuf.ssl_wrapper_pb2 import SSL_WrapperPacket


@dataclass
class FilteredDataWrapper:
    ball_status: BallDataEstimated
    own_robots_status: List[RobotDataEstimated]
    opp_robots_status: List[RobotDataEstimated]

    def __str__(self):
        return (
            "filteredDataWrapper: \n   ball_status: "
            + str(self.ball_status)
            + "\n   own_robots_status: "
            + str(self.own_robots_status)
            + "\n   opp_robots_status: "
            + str(self.opp_robots_status)
            + "\n"
        )


class World:
    """Represents the current state of the world."""

    def __init__(self, num_robots=7, is_blue=True):
        filter = SimpleFilter()
        self.own_robots_status = []
        self.opp_robots_status = []
        self.ball_status = BallTracker(filter)
        self.is_blue = is_blue
        self.num_robots = num_robots
        for i in range(num_robots):
            self.own_robots_status.append(RobotTracker(filter))
            self.opp_robots_status.append(RobotTracker(filter))

    def get_status(self) -> FilteredDataWrapper:
        """Returns the current world state."""
        return FilteredDataWrapper(
            self.ball_status.get(),
            [tracker.get() for tracker in self.own_robots_status],
            [tracker.get() for tracker in self.opp_robots_status],
        )

    def update_from_protobuf(self, raw_data: bytes) -> FilteredDataWrapper:
        packet = SSL_WrapperPacket()
        packet.ParseFromString(raw_data)
        frame = packet.detection
        if frame is None:
            return None
        return self.update_vision_data(frame)

    def update_vision_data(self, frame: SSL_DetectionFrame) -> FilteredDataWrapper:
        """Updates the world state from vision data."""
        camera_id = frame.camera_id
        time = frame.t_capture
        for ball in frame.balls:
            self.ball_status.add(
                BallDataRaw(time, camera_id, (ball.x, ball.y, ball.z), ball.confidence)
            )
        for robot in frame.robots_yellow:
            if robot.robot_id < 0 or robot.robot_id >= self.num_robots:
                continue
            if self.is_blue:
                self.opp_robots_status[robot.robot_id].add(
                    RobotDataRaw(time, camera_id, (robot.x, robot.y), robot.orientation)
                )
            else:
                self.own_robots_status[robot.robot_id].add(
                    RobotDataRaw(time, camera_id, (robot.x, robot.y), robot.orientation)
                )
        for robot in frame.robots_blue:
            if robot.robot_id < 0 or robot.robot_id >= self.num_robots:
                continue
            if self.is_blue:
                self.own_robots_status[robot.robot_id].add(
                    RobotDataRaw(time, camera_id, (robot.x, robot.y), robot.orientation)
                )
            else:
                self.opp_robots_status[robot.robot_id].add(
                    RobotDataRaw(time, camera_id, (robot.x, robot.y), robot.orientation)
                )
        return self.get_status()
