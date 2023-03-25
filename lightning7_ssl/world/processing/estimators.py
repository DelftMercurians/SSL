import abc
from collections import OrderedDict
from dataclasses import dataclass
from typing import List, Optional

from ...vecMath.vec_math import Vec2, Vec3


@dataclass
class RobotDataRaw:
    """
    a dataclass to store raw data from ssl vision, this contact can be modified based on real needs.
    for now only time and position are included, but more information can be added, and if other data need to
    go through the filter, it should be intergrated into this dataclass.
    """

    #: time the data is captured unit: second
    time_stamp: float
    #: camera id
    camara_id: int
    #: position of the robot
    position: Vec2
    #: orientation of the robot [-pi,pi]
    orientation: float


@dataclass
class RobotData:
    """
    a dataclass to store estimated data from ssl vision, this contact can be modified based on real needs.
    """

    #: position of the robot
    position: Vec2
    #: orientation of the robot [-pi,pi]
    orientation: float
    #: velocity of the robot
    velocity: Vec2
    #: angular speed of the robot
    angular_speed: float


@dataclass
class BallDataRaw:
    """
    a dataclass to store raw data from ssl vision, this contact can be modified based on real needs.
    """

    #: time the data is captured unit: second
    time_stamp: float
    #: camera id
    camara_id: int
    #: position of the ball
    position: Vec3
    #: confidence of the ball [0,1]
    confidence: float


@dataclass
class BallData:
    """
    A dataclass to store estimated data from ssl vision, this contact can be modified based on real needs.

    Confidence is not included because it is not needed for now.
    """

    #: position of the ball
    position: Vec3
    #: velocity of the ball
    velocity: Vec3


class StatusEstimator(metaclass=abc.ABCMeta):
    """
    interface for status estimater, including a ball filter and a robot filter
    """

    @abc.abstractmethod
    def ball_filter(self, raw_data: OrderedDict[float, List[BallDataRaw]]) -> Optional[BallData]:
        """
        filter the ball data

        Args:
            raw_data: the raw data from ssl vision

        Returns: the estimated data
        """
        pass

    @abc.abstractmethod
    def robot_filter(self, raw_data: OrderedDict[float, List[RobotDataRaw]]) -> Optional[RobotData]:
        """
        filter the robot data

        Args:
            raw_data: the raw data from ssl vision
        Returns: the estimated data
        """
        pass
