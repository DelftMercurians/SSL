from typing import List, Optional

from google.protobuf.message import DecodeError

from lightning7_ssl.cfg import GlobalConfig
from lightning7_ssl.vis.data_store import DataStore

from ..control_client.protobuf.ssl_detection_pb2 import SSL_DetectionFrame
from ..control_client.protobuf.ssl_geometry_pb2 import SSL_GeometryData
from ..control_client.protobuf.ssl_wrapper_pb2 import SSL_WrapperPacket
from ..vecMath.vec_math import Vec2, Vec3
from ..world.processing.trackers import BallTracker, RobotTracker
from .ctx import WorldCtx
from .frame import Frame
from .geometry import FieldCircularArc, FieldGeometry, FieldLinesSegment
from .processing import BallDataRaw, RobotDataRaw
from .processing.simple_estimator import SimpleEstimator


class UninitializedError(Exception):
    """Raised when an object in the world is accessed before it is initialized, ie.
    before a detection frame is received."""

    pass


class World:
    """Processes SSL detection/geometry packets, performs any cleanup and processings
    necessary, and provides access to the current frame containing the state of the
    world.

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
    data_store: DataStore
    _last_frame: Optional[Frame] = None  # Use the `frame` for accessing this
    ctx: WorldCtx

    def __init__(self, data_store: DataStore, config: GlobalConfig):
        self.data_store = data_store
        self.is_blue = config.team_color == "blue"
        self.num_robots = config.num_players
        self.update_geom_only_once = True
        self.ctx = WorldCtx([])

        filter = SimpleEstimator()

        # Robots
        self.own_robots_status = []
        self.opp_robots_status = []
        self.ball_status = BallTracker(filter)
        for i in range(self.num_robots):
            self.own_robots_status.append(RobotTracker(filter))
            self.opp_robots_status.append(RobotTracker(filter))

        # Field geometry and lines
        self.field_geometry = None
        self.field_line_segments = []
        self.field_circular_arcs = []

    #################
    # Access methods
    #################

    def frame(self) -> Frame:
        """Returns the current `Frame` of the world.

        Raises:
            UninitializedError: If the frame is accessed before it is initialized.
        """
        if self._last_frame is None:
            raise UninitializedError("Frame accessed before it is initialized")
        return self._last_frame

    #################
    # Update methods
    #################

    def update_from_protobuf(self, raw_data: bytes) -> None | Frame:
        """
        Updates the world state from raw protobuf data. If the packet contains vision
        data, it updates the world state and returns the new frame. Otherwise, it
        returns None.

        Args:
            raw_data: The raw protobuf data in bytes. must be a `SSL_WrapperPacket`.
        """
        packet = SSL_WrapperPacket()
        try:
            packet.ParseFromString(raw_data)
        except DecodeError:
            return None

        if packet.detection is not None:
            return self.update_vision_data(packet.detection)
        if packet.geometry is not None and (not self.update_geom_only_once or self.field_geometry is None):
            self.update_geometry(packet.geometry)
        return None

    def update_vision_data(self, frame: SSL_DetectionFrame) -> Optional[Frame]:
        """
        Updates the world state from vision data. It unpacks the data and updates each
        robot and ball tracker.

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

        # Check if any of the get() calls return None, if not create a new frame
        try:
            ball_state = self.ball_status.get()
            assert ball_state is not None
            own_players = []
            for player in self.own_robots_status:
                player_state = player.get()
                assert player_state is not None
                own_players.append(player_state)
            opp_players = []
            for player in self.opp_robots_status:
                player_state = player.get()
                assert player_state is not None
                opp_players.append(player_state)
            self._last_frame = Frame(ball=ball_state, own_players=own_players, opp_players=opp_players)
            self.ctx.frames.append(self._last_frame)
            # Try to update data store
            self.data_store.update_player_and_ball_states(self._last_frame)

            return self._last_frame
        except AssertionError:
            return None

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

        # Try to update data store
        self.data_store.update_geom(
            self.field_geometry,
            self.field_line_segments,
            self.field_circular_arcs,
        )
