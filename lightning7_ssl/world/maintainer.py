from typing import List, Optional
from google.protobuf.message import DecodeError
from dataclasses import dataclass
from .common import *
from .simple_filter import SimpleFilter
from ..control_client.protobuf.ssl_detection_pb2 import SSL_DetectionFrame
from ..control_client.protobuf.ssl_wrapper_pb2 import SSL_WrapperPacket


@dataclass
class FilteredDataWrapper:
    """Represents the current state of the world.
    it's the fianl diliverable it can provide for other modules.
    """

    #: The ball status.
    ball_status: BallDataEstimated
    #: The own robots status.
    own_robots_status: List[RobotDataEstimated]
    #: The opponent robots status.
    opp_robots_status: List[RobotDataEstimated]

    def __str__(self):
        """
        a string representation of the data
        Returns: the string representation of the data
        """
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
    """Represents the current state of the world.response for assign the data to the right robot and ball, only this class
    keeps track of different robots and ball, anything below it is anonymous.
    Attributes:
        own_robots_status: A list of RobotTrackers for the own robots.
        opp_robots_status: A list of RobotTrackers for the opponent robots.
        ball_status: A BallTracker for the ball.
        is_blue: Whether the team is blue or not.
        num_robots: The number of robots on the team.
    """

    own_robots_status: List[RobotTracker]
    opp_robots_status: List[RobotTracker]
    ball_status: BallTracker
    is_blue: bool
    num_robots: int

    def __init__(self, num_robots=6, is_blue=True):
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
        """Returns the current world state.

        Usage:
            call self.ball_status/own_robots_status/opp_robots_status
        """
        return FilteredDataWrapper(
            self.ball_status.get(),
            [tracker.get() for tracker in self.own_robots_status],
            [tracker.get() for tracker in self.opp_robots_status],
        )

    def update_from_protobuf(self, raw_data: bytes) -> Optional[FilteredDataWrapper]:
        """Updates the world state from raw protobuf data.
        Args:
            raw_data: The raw protobuf data in bytes.
        Raises:
            DecodeError: If the data is not a valid SSL_WrapperPacket.
        """
        packet = SSL_WrapperPacket()
        try:
            packet.ParseFromString(raw_data)
        except DecodeError:
            return None
        frame = packet.detection
        if frame is None:
            return None
        return self.update_vision_data(frame)

    def update_vision_data(self, frame: SSL_DetectionFrame) -> FilteredDataWrapper:
        """Updates the world state from vision data. it depack the data and assign it
        to the right robot and ball.
        Args:
            frame: The SSL_DetectionFrame to update from.
        """
        camera_id = frame.camera_id
        time = frame.t_capture
        for ball in frame.balls:
            self.ball_status.add(
                BallDataRaw(
                    time, camera_id, Vec3(ball.x, ball.y, ball.z), ball.confidence
                )
            )

        own_robots_status_frame = (
            frame.robots_blue if self.is_blue else frame.robots_yellow
        )
        for robot in own_robots_status_frame:
            if robot.robot_id not in range(self.num_robots):
                continue
            self.own_robots_status[robot.robot_id].add(
                RobotDataRaw(time, camera_id, Vec2(robot.x, robot.y), robot.orientation)
            )
        opp_robots_status_frame = (
            frame.robots_yellow if self.is_blue else frame.robots_blue
        )
        for robot in opp_robots_status_frame:
            if robot.robot_id not in range(self.num_robots):
                continue
            self.opp_robots_status[robot.robot_id].add(
                RobotDataRaw(time, camera_id, Vec2(robot.x, robot.y), robot.orientation)
            )
        return self.get_status()

    def get_team_position(self):
        """Returns the current position of the own robots."""
        return [tracker.get().position for tracker in self.own_robots_status]

    def get_team_vel(self):
        """Returns the current speed of the own robots."""
        return [tracker.get().velocity for tracker in self.own_robots_status]

    def get_opp_position(self):
        """Returns the current position of the opponent robots."""
        return [tracker.get().position for tracker in self.opp_robots_status]

    def get_opp_vel(self):
        """Returns the current speed of the opponent robots."""
        return [tracker.get().velocity for tracker in self.opp_robots_status]
