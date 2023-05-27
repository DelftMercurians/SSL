from unittest.mock import Mock

from lightning7_ssl.vecMath.vec_math import Vec2, Vec3
from lightning7_ssl.world import BallData, Frame, RobotData, WorldCtx


def to_vec2(pos: tuple[float, float] | Vec2) -> Vec2:
    if isinstance(pos, Vec2):
        return pos
    else:
        return Vec2(*pos)


def to_vec3(pos: tuple[float, float] | Vec3 | Vec2 | tuple[float, float, float]) -> Vec3:
    if isinstance(pos, Vec3):
        return pos
    elif isinstance(pos, Vec2):
        return Vec3(pos.x, pos.y, 0.0)
    else:
        return Vec3(*pos)


def mock_frame(
    *,
    ball_pos: tuple[float, float] | Vec2 | Vec3 = (0.0, 0.0),
    own_pos: list[tuple[float, float]] | list[Vec2] = [(0.0, 0.0)],
    opp_pos: list[tuple[float, float]] | list[Vec2] = [(0.0, 0.0)],
    ball: tuple[tuple[float, float], tuple[float, float]] | tuple[Vec2, Vec2] | BallData | None = None,
    own: list[tuple[tuple[float, float], tuple[float, float]]]
    | list[tuple[Vec2, Vec2]]
    | list[RobotData]
    | None = None,
    opp: list[tuple[tuple[float, float], tuple[float, float]]]
    | list[tuple[Vec2, Vec2]]
    | list[RobotData]
    | None = None,
) -> Frame:
    """Create a mock frame from the given data.

    There are three ways to specify the ball position and velocity:
    1. As a tuple of tuples of floats, e.g. `((0.0, 0.0), (0.0, 0.0))`, using the `ball_pos`,
    `own_pos`, and `opp_pos` arguments. With this format, only positions can be specified,
    and velocities will be set to `(0.0, 0.0)`.
    2. As a tuple of `Vec2`s, e.g. `(Vec2(0.0, 0.0), Vec2(0.0, 0.0))`, or tuple of tuples of
    floats, e.g. `((0.0, 0.0), (0.0, 0.0))`, using the `ball`, `own`, and `opp` arguments.
    With this format, both positions and velocities can be specified.
    3. As a `BallData`/`RobotData` object, using the `ball`, `own`, and `opp` arguments.
    """
    ball = (
        BallData(to_vec3(ball[0]), to_vec3(ball[1]))
        if isinstance(ball, tuple)
        else ball
        if ball is not None
        else BallData(to_vec3(ball_pos), Vec3(0.0, 0.0, 0.0))
    )
    if own is not None:
        own = [
            RobotData(position=to_vec2(pos[0]), velocity=to_vec2(pos[1]), orientation=0, angular_speed=0)
            if isinstance(pos, tuple)
            else pos
            for pos in own
        ]
    else:
        own = [
            RobotData(position=to_vec2(pos), velocity=Vec2(0.0, 0.0), orientation=0, angular_speed=0)
            for pos in own_pos
        ]
    if opp is not None:
        opp = [
            RobotData(position=to_vec2(pos[0]), velocity=to_vec2(pos[1]), orientation=0, angular_speed=0)
            if isinstance(pos, tuple)
            else pos
            for pos in opp
        ]
    else:
        opp = [
            RobotData(position=to_vec2(pos), velocity=Vec2(0.0, 0.0), orientation=0, angular_speed=0)
            for pos in opp_pos
        ]
    return Frame(
        ball=ball,
        own_players=own,
        opp_players=opp,
    )


class MockWorldBuilder:
    """A class for building mock `WorldCtx` objects."""

    def __init__(self):
        self.frames = []

    def add_frame(
        self,
        *,
        ball_pos: tuple[float, float] | Vec2 | Vec3 = (0.0, 0.0),
        own_pos: list[tuple[float, float]] | list[Vec2] = [(0.0, 0.0)],
        opp_pos: list[tuple[float, float]] | list[Vec2] = [(0.0, 0.0)],
        ball: tuple[tuple[float, float], tuple[float, float]] | tuple[Vec2, Vec2] | BallData | None = None,
        own: list[tuple[tuple[float, float], tuple[float, float]]]
        | list[tuple[Vec2, Vec2]]
        | list[RobotData]
        | None = None,
        opp: list[tuple[tuple[float, float], tuple[float, float]]]
        | list[tuple[Vec2, Vec2]]
        | list[RobotData]
        | None = None,
    ) -> "MockWorldBuilder":
        """Add a frame to the mock world.

        For details on the arguments, see `mock_frame`."""
        self.frames.append(
            mock_frame(
                ball_pos=ball_pos,
                own_pos=own_pos,
                opp_pos=opp_pos,
                ball=ball,
                own=own,
                opp=opp,
            )
        )
        return self

    def finish(self) -> WorldCtx:
        return Mock(wraps=WorldCtx(self.frames))


def start_mock_world() -> MockWorldBuilder:
    """Start a mock world builder.

    Usage:
    >>> start_mock_world().add_frame().add_frame().finish()
    """
    return MockWorldBuilder()


def mock_world_one_frame(
    *,
    ball_pos: tuple[float, float] | Vec2 | Vec3 = (0.0, 0.0),
    own_pos: list[tuple[float, float]] | list[Vec2] = [(0.0, 0.0)],
    opp_pos: list[tuple[float, float]] | list[Vec2] = [(0.0, 0.0)],
    ball: tuple[tuple[float, float], tuple[float, float]] | tuple[Vec2, Vec2] | BallData | None = None,
    own: list[tuple[tuple[float, float], tuple[float, float]]]
    | list[tuple[Vec2, Vec2]]
    | list[RobotData]
    | None = None,
    opp: list[tuple[tuple[float, float], tuple[float, float]]]
    | list[tuple[Vec2, Vec2]]
    | list[RobotData]
    | None = None,
) -> WorldCtx:
    """Create a mock world with one frame from the given data.

    For details on the arguments, see `mock_frame`."""
    return Mock(
        wraps=WorldCtx(
            [mock_frame(ball_pos=ball_pos, own_pos=own_pos, opp_pos=opp_pos, ball=ball, own=own, opp=opp)]
        )
    )


def mock_world_no_frames() -> WorldCtx:
    """Create a mock world with no frames."""
    return Mock(wraps=WorldCtx([]))
