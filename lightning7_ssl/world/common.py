from dataclasses import dataclass, field
from typing import List, Tuple
from collections import OrderedDict
from ..vecMath.vec_math import Vec2, Vec3
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
        a dataclass to store estimated data from ssl vision, this contact can be modified based on real needs.
        confidence is not included because it is not needed for now.

    """

    #: position of the ball
    position: Vec3
    #: velocity of the ball
    velocity: Vec3

    """
    a string representation of the data
    Returns: the string representation of the data
    """
    def __str__(self):
        return (
            "BallDataEstimated: [pos: "
            + str(self.position)
            + " velocity: "
            + str(self.velocity)
            + "]"
        )


class StatusEstimater(metaclass=abc.ABCMeta):
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
    filter: StatusEstimater

    def __init__(self, filter: StatusEstimater, limit=500):
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
    filter: StatusEstimater


    def __init__(self, filter: StatusEstimater, limit=100):
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
