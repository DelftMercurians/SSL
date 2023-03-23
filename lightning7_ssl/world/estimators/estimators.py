from dataclasses import dataclass, field
from typing import List, Tuple
from collections import OrderedDict
from ...vecMath.vec_math import Vec2, Vec3
import abc


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

    def __str__(self):
        """
        a string representation of the data
        Returns: the string representation of the data
        """
        return (
            "RobotDataRaw: [time: "
            + str(self.time_stamp)
            + " camera: "
            + str(self.camara_id)
            + " pos: "
            + str(self.position)
            + " ori: "
            + str(self.orientation)
            + "]\n"
        )


@dataclass
class RobotDataEstimated:
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

    def __str__(self):
        """
        a string representation of the data
        Returns: the string representation of the data
        """
        return (
            "RobotDataEstimated: [pos: "
            + str(self.position)
            + " ori: "
            + str(self.orientation)
            + " velocity: "
            + str(self.velocity)
            + " spin: "
            + str(self.angular_speed)
            + "]\n"
        )


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

    def __str__(self):
        """
        a string representation of the data
        Returns: the string representation of the data
        """
        return (
            "BallDataRaw: [time: "
            + str(self.time_stamp)
            + " camera: "
            + str(self.camara_id)
            + " pos: "
            + str(self.position)
            + " confidence: "
            + str(self.confidence)
            + "]\n"
        )


@dataclass
class BallDataEstimated:
    """
    A dataclass to store estimated data from ssl vision, this contact can be modified based on real needs.

    Confidence is not included because it is not needed for now.
    """

    #: position of the ball
    position: Vec3
    #: velocity of the ball
    velocity: Vec3

    def __str__(self):
        """
        a string representation of the data

        Returns: the string representation of the data
        """
        return (
            "BallDataEstimated: [pos: "
            + str(self.position)
            + " velocity: "
            + str(self.velocity)
            + "]"
        )


class StatusEstimator(metaclass=abc.ABCMeta):
    """
    interface for status estimater, including a ball filter and a robot filter
    """

    @abc.abstractmethod
    def ball_filter(
        self, raw_data: OrderedDict[float, List[BallDataRaw]]
    ) -> BallDataEstimated:
        """
        filter the ball data

        Args:
            raw_data: the raw data from ssl vision

        Returns: the estimated data
        """
        pass

    @abc.abstractmethod
    def robot_filter(
        self, raw_data: OrderedDict[float, List[RobotDataRaw]]
    ) -> RobotDataEstimated:
        """
        filter the robot data

        Args:
            raw_data: the raw data from ssl vision
        Returns: the estimated data
        """
        pass
