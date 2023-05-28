from typing import List, Optional

from google.protobuf.message import DecodeError

from lightning7_ssl import cfg

from ..control_client.protobuf.ssl_detection_pb2 import SSL_DetectionFrame
from ..control_client.protobuf.ssl_geometry_pb2 import SSL_GeometryData
from ..control_client.protobuf.ssl_wrapper_pb2 import SSL_WrapperPacket
from ..vecMath.vec_math import Vec2, Vec3
from ..world.processing.trackers import BallTracker, RobotTracker
from .geometry import FieldCircularArc, FieldGeometry, FieldLinesSegment
from .processing import BallDataRaw, RobotDataRaw
from .processing.estimators import BallData, RobotData
from .processing.simple_estimator import SimpleEstimator


class UninitializedError(Exception):
    """Raised when an object in the world is accessed before it is initialized, ie.
    before a detection frame is received."""

    pass


class World:
    """Represents the current state of the world.response for assign the data to the
    right robot and ball, only this class
    keeps track of different robots and ball, anything below it is anonymous.

    Attributes:
        own_robots_status: A list of RobotTrackers for the own robots.

        opp_robots_status: A list of RobotTrackers for the opponent robots.

        ball_status: A BallTracker for the ball.

        is_blue: Whether the team is blue or not.

        num_robots: The number of robots on the team.

        update_geom_only_once: Whether to update the field geometry only once or not.
    """

    is_blue: bool
    num_robots: int
    update_geom_only_once: bool

    own_robots_status: List[RobotTracker]
    opp_robots_status: List[RobotTracker]
    field_geometry: Optional[FieldGeometry]
    field_line_segments: List[FieldLinesSegment]
    field_circular_arcs: List[FieldCircularArc]
    ball_status: BallTracker

    def __init__(self, num_robots=6, is_blue=True, update_geom_only_once=True):
        self.is_blue = is_blue
        self.num_robots = num_robots
        self.update_geom_only_once = update_geom_only_once

        filter = SimpleEstimator()

        # Robots
        self.own_robots_status = []
        self.opp_robots_status = []
        self.ball_status = BallTracker(filter)
        for i in range(num_robots):
            self.own_robots_status.append(RobotTracker(filter))
            self.opp_robots_status.append(RobotTracker(filter))

        # Field geometry and lines
        self.field_geometry = None
        self.field_line_segments = []
        self.field_circular_arcs = []

    #################
    # Access methods
    #################

    def get_ball_state(self) -> Optional[BallData]:
        """Returns the current state of the ball or None if uninitialized."""
        return self.ball_status.get()

    def get_team_state(self) -> Optional[List[RobotData]]:
        """Returns the current state of the own robots or None if uninitialized."""
        states = [tracker.get() for tracker in self.own_robots_status]
        if None in states:
            return None
        return states

    def get_opp_state(self) -> Optional[List[RobotData]]:
        """Returns the current state of the opponent robots or None if uninitialized."""
        states = [tracker.get() for tracker in self.opp_robots_status]
        if None in states:
            return None
        return states

    def get_robot_pos(self, id: int) -> Vec2:
        """Returns the current position of the robot with the given id.

        This will raise an exception if the robot is not initialized."""
        try:
            return self.own_robots_status[id].get().position
        except AttributeError:
            # raise UninitializedError("Robot not initialized")
            pass

    def get_robot_vel(self, id: int) -> Vec2:
        """Returns the current velocity of the robot with the given id.

        This will raise an exception if the robot is not initialized."""
        try:
            return self.own_robots_status[id].get().velocity
        except AttributeError:
            # raise UninitializedError("Robot not initialized")
            pass

    def get_robot_heading(self, id: int) -> float:
        """Returns the current heading of the robot with the given id.

        This will raise an exception if the robot is not initialized."""
        try:
            return self.own_robots_status[id].get().orientation
        except AttributeError:
            # raise UninitializedError("Robot not initialized")
            pass

    def get_team_position(self) -> List[Vec2]:
        """Returns the current position of the own robots.

        This will raise an exception if a robot is not initialized."""
        try:
            return [tracker.get().position for tracker in self.own_robots_status]
        except AttributeError:
            # raise UninitializedError("Robot not initialized")
            pass

    def get_team_vel(self) -> List[Vec2]:
        """Returns the current speed of the own robots.

        This will raise an exception if a robot is not initialized."""
        try:
            return [tracker.get().velocity for tracker in self.own_robots_status]
        except AttributeError:
            # raise UninitializedError("Robot not initialized")
            pass

    def get_opp_position(self) -> List[Vec2]:
        """Returns the current position of the opponent robots.

        This will raise an exception if a robot is not initialized."""
        try:
            return [tracker.get().position for tracker in self.opp_robots_status]
        except AttributeError:
            # raise UninitializedError("Robot not initialized")
            pass

    def get_opp_vel(self) -> List[Vec2]:
        """Returns the current speed of the opponent robots.

        This will raise an exception if a robot is not initialized."""
        try:
            return [tracker.get().velocity for tracker in self.opp_robots_status]
        except AttributeError:
            # raise UninitializedError("Robot not initialized")
            pass

    #################
    # Update methods
    #################

    def update_from_protobuf(self, raw_data: bytes) -> None:
        """
        Updates the world state from raw protobuf data.

        Args:
            raw_data: The raw protobuf data in bytes.
        """
        packet = SSL_WrapperPacket()
        try:
            packet.ParseFromString(raw_data)
        except DecodeError:
            return

        if packet.detection is not None:
            self.update_vision_data(packet.detection)
        if packet.geometry is not None and (not self.update_geom_only_once or self.field_geometry is None):
            print("update_geometry")
            self.update_geometry(packet.geometry)

    def update_vision_data(self, frame: SSL_DetectionFrame) -> None:
        """
        Updates the world state from vision data. it depack the data and assign it
        to the right robot and ball.

        Args:
            frame: The SSL_DetectionFrame to update from.
        """
        camera_id = frame.camera_id
        time = frame.t_capture
        for ball in frame.balls:
            self.ball_status.add(BallDataRaw(time, camera_id, Vec3(ball.x, ball.y, ball.z), ball.confidence))

        own_robots_status_frame = frame.robots_blue if self.is_blue else frame.robots_yellow
        for robot in own_robots_status_frame:
            if robot.robot_id not in range(self.num_robots):
                continue
            self.own_robots_status[robot.robot_id].add(
                RobotDataRaw(time, camera_id, Vec2(robot.x, robot.y), robot.orientation)
            )
        opp_robots_status_frame = frame.robots_yellow if self.is_blue else frame.robots_blue
        for robot in opp_robots_status_frame:
            if robot.robot_id not in range(self.num_robots):
                continue
            self.opp_robots_status[robot.robot_id].add(
                RobotDataRaw(time, camera_id, Vec2(robot.x, robot.y), robot.orientation)
            )
        # Try to update data store
        cfg.data_store.update_player_and_ball_states()

    def update_geometry(self, geometry: SSL_GeometryData) -> None:
        """
        Updates the world state from geometry data.
        """
        fg = geometry.field

        self.field_geometry = FieldGeometry(
            fg.field_length,
            fg.field_width,
            fg.goal_width,
            fg.goal_depth,
            fg.boundary_width,
            fg.penalty_area_depth,
            fg.penalty_area_width,
        )

        # Append each line segment into the field_ling_segments list
        for i, segment in enumerate(fg.field_lines):
            line = FieldLinesSegment(
                i,
                segment.name,
                Vec2(segment.p1.x, segment.p1.y),
                Vec2(segment.p2.x, segment.p2.y),
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

        print("Received field geometry")
        # Try to update data store
        cfg.data_store.update_geom()
