from dataclasses import dataclass


@dataclass
class World:
    """
    Dimensions of the football field.
    """

    fieldWidth: float
    fieldLength: float
    goalWidth: float
    goalLength: float
    boundary_width: float  # Distance between field and inner white line field


@dataclass
class BallInfo:
    """
    Position information of the ball.
    """

    x: float
    y: float
    v_x: float
    v_y: float
    confidence: float


@dataclass
class RobotState:
    """
    State of the robots.
    """

    x: float
    y: float
    v_x: float
    v_y: float
    w: float
    yaw: float  # [-pi,pi]
    confidence: float  # [0,1]
