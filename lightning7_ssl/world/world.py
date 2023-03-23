from collections import OrderedDict
from typing import List, Optional
from google.protobuf.message import DecodeError
from dataclasses import dataclass

from lightning7_ssl.vecMath.vec_math import Vec2, Vec3
from .estimators.simple_filter import SimpleFilter
from ..control_client.protobuf.ssl_detection_pb2 import SSL_DetectionFrame
from ..control_client.protobuf.ssl_wrapper_pb2 import SSL_WrapperPacket
from .estimators import (
    StatusEstimator,
    BallDataEstimated,
    RobotDataEstimated,
    BallDataRaw,
    RobotDataRaw,
)


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


@dataclass
class FieldGeometry:
    """
    A dataclass to store field geometry data from ssl vision.
    """

    # Excluded field line segments, arcs, and penalty area for now, can be added later
    field_length: int
    field_width: int
    goal_width: int
    goal_depth: int
    boundary_width: int
    penalty_area_depth: int
    penalty_area_width: int

    def __str__(self):
        """
        A string representation of the data

        Returns:
            the string representation of the data
        """
        return (
            "FieldGeometry: [field_length: "
            + str(self.field_length)
            + " field_width: "
            + str(self.field_width)
            + " goal_width: "
            + str(self.goal_width)
            + " goal_depth: "
            + str(self.goal_depth)
            + " boundary_width: "
            + str(self.boundary_width)
            + " penalty_area_width: "
            + str(self.penalty_area_width)
            + " penalty_area_depth: "
            + str(self.penalty_area_depth)
            + "]\n"
        )


@dataclass
class FieldLinesSegment:
    """
    A dataclass to store a single line segments.

    @params:
        p1: Start point of segment
        p2: End point of segment
    """

    index: int
    name: str
    p1: Vec2
    p2: Vec2
    thickness: float

    def __str__(self) -> str:
        """
        A string representation of the data.
        """
        return (
            "LineSegment ["
            + str(self.index)
            + "]: "
            + str(self.name)
            + " p1: "
            + str(self.p1.vec)
            + " p2: "
            + str(self.p2.vec)
            + " thickness: "
            + str(self.thickness)
            + "\n"
        )


@dataclass
class FieldCircularArc:
    """
    A class to store a single field arc.

    @params:
        a1: Start angle in counter-clockwise order.
        a2: End angle in counter-clockwise order.
    """

    index: int
    name: str
    center: Vec2
    radius: float
    a1: float
    a2: float
    thickness: float

    def __str__(self) -> str:
        return (
            "CircularArc ["
            + str(self.index)
            + "]: "
            + str(self.name)
            + " center: "
            + str(self.center.vec)
            + " radius: "
            + str(self.radius)
            + " a1: "
            + str(self.a1)
            + " a2: "
            + str(self.a2)
            + " thickness: "
            + str(self.thickness)
            + "\n"
        )


class BallTracker:
    """
    the tracker for ball, it keeps a specific filter strategy and also responsible for the data storage
    """

    #: the data storage, it is a ordered dict, the key is the time stamp, the value is a list of data because it
    #  may came from different cameras
    record: OrderedDict[float, List[BallDataRaw]]
    #: the capacity of the storage, related to the filter process speed.
    capacity: int
    #: the filter strategy
    filter: StatusEstimator

    def __init__(self, filter: StatusEstimator, limit=500):
        """
        init the tracker

        Args:
            filter:  the filter strategy
            limit:  the capacity of the storage
        """
        self.record = OrderedDict()
        self.capacity = limit
        self.filter = filter

    def add(self, ball_data: BallDataRaw):
        """
        add a new data to the storage
        while maintaining the max capacity

        Args:
            ball_data: the new data
        """
        if len(self.record) == self.capacity:
            self.record.popitem(last=False)
        time = ball_data.time_stamp
        if time in self.record:
            self.record[time].append(ball_data)
        else:
            self.record[time] = [ball_data]

    def get(self):
        """
        get the most related data
        Returns: the estimated data
        TODO: probably need to the request time into consideration
        """
        return self.filter.ball_filter(self.record)


class RobotTracker:
    """
    the tracker for robot, it keeps a specific filter strategy and also responsible for the data storage
    """

    #: the data storage, it is a ordered dict, the key is the time stamp, the value is a list of data
    record: OrderedDict[float, List[RobotDataRaw]]
    #: the capacity of the storage, related to the filter process speed.
    capacity: int
    #: the filter strategy
    filter: StatusEstimator

    def __init__(self, filter: StatusEstimator, limit=100):
        """
        init the tracker

        Args:
            filter:  the filter strategy
            limit:  the capacity of the storage
        """
        self.record = OrderedDict()
        self.capacity = limit
        self.filter = filter

    def add(self, robot_data: RobotDataEstimated):
        """
        add a new data to the storage while maintaining the max capacity.

        Args:
            robot_data:  the new data
        """
        # if it is full, remove the oldest one
        if len(self.record) == self.capacity:
            self.record.popitem(last=False)
        time = robot_data.time_stamp
        if time in self.record:
            self.record[time].append(robot_data)
        else:
            self.record[time] = [robot_data]

    def get(self):
        """
        get the most related data
        Returns: the estimated data
        TODO: probably need to the request time into consideration
        """
        return self.filter.robot_filter(self.record)


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
    field_geometry: FieldGeometry
    field_line_segments: List[FieldLinesSegment]
    field_circular_arcs: List[FieldCircularArc]
    ball_status: BallTracker
    is_blue: bool
    num_robots: int

    def __init__(self, num_robots=6, is_blue=True):
        filter = SimpleFilter()

        # Robots
        self.own_robots_status = []
        self.opp_robots_status = []
        self.ball_status = BallTracker(filter)
        self.is_blue = is_blue
        self.num_robots = num_robots
        for i in range(num_robots):
            self.own_robots_status.append(RobotTracker(filter))
            self.opp_robots_status.append(RobotTracker(filter))

        # Field geometry and lines
        self.field_geometry = None
        self.field_line_segments = []
        self.field_circular_arcs = []

    def set_geom(self, raw_data: bytes) -> None:
        """
        Sets the geometry of the field from raw protobuf data. The data is updated in attributes
            :field_geometry:

            :field_line_segments:

            :field_circular_arcs:

        :param:
            raw_data: The raw protobuf data in bytes.
        """
        packet = SSL_WrapperPacket()
        packet.ParseFromString(raw_data)
        fg = packet.geometry.field

        self.field_geometry = FieldGeometry(
            fg.field_length / 1000,
            fg.field_width / 1000,
            fg.goal_width / 1000,
            fg.goal_depth / 1000,
            fg.boundary_width / 1000,
            fg.penalty_area_depth / 1000,
            fg.penalty_area_width / 1000,
        )

        # Append each line segment into the field_ling_segments list
        for i, segment in enumerate(fg.field_lines):
            line = FieldLinesSegment(
                i,
                segment.name,
                Vec2(segment.p1.x / 1000, segment.p1.y / 1000),
                Vec2(segment.p2.x / 1000, segment.p2.y / 1000),
                segment.thickness,
            )
            self.field_line_segments.append(line)

        for i, arc in enumerate(fg.field_arcs):
            t = FieldCircularArc(
                i,
                arc.name,
                Vec2(arc.center.x, arc.center.y),
                arc.radius,
                arc.a1,
                arc.a2,
                arc.thickness,
            )
            self.field_circular_arcs.append(t)

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
        """
        Updates the world state from raw protobuf data.

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
        """
        Updates the world state from vision data. it depack the data and assign it
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
