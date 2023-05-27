from dataclasses import dataclass

from lightning7_ssl.vecMath.vec_math import Vec2, Vec3


@dataclass
class RobotData:
    """Stores estimated data from ssl vision, this contact can be modified based on real
    needs."""

    #: position of the robot
    position: Vec2
    #: orientation of the robot [-pi,pi]
    orientation: float
    #: velocity of the robot
    velocity: Vec2
    #: angular speed of the robot
    angular_speed: float


@dataclass
class BallData:
    """Stores estimated data from ssl vision, this contact can be modified based on real
    needs.

    Confidence is not included because it is not needed for now.
    """

    #: position of the ball
    position: Vec3
    #: velocity of the ball
    velocity: Vec3


@dataclass
class Frame:
    """Stores the state of the world for a single frame."""

    ball: BallData
    own_players: list[RobotData]
    opp_players: list[RobotData]
