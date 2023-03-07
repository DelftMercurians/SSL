from dataclasses import dataclass, field
from typing import List, Tuple
from collections import OrderedDict
from ..vecMath.vec_math import Vec2, Vec3
import abc

@dataclass
class RobotDataRaw:
    time_stamp: float
    camara_id: int
    position: Vec2
    orientation: float  # [-pi,pi]

    def __str__(self):
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
    position: Vec2
    orientation: float
    velocity: Vec2
    angular_speed: float

    def __str__(self):
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
    time_stamp: float
    camara_id: int
    position: Vec3
    confidence: float

    def __str__(self):
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
    position: Vec3
    velocity: Vec3

    def __str__(self):
        return (
            "BallDataEstimated: [pos: "
            + str(self.position)
            + " velocity: "
            + str(self.velocity)
            + "]"
        )


class StatusEstimater(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def ball_filter(
        self, raw_data: OrderedDict[float, List[BallDataRaw]]
    ) -> BallDataEstimated:
        pass

    @abc.abstractmethod
    def robot_filter(
        self, raw_data: OrderedDict[float, List[RobotDataRaw]]
    ) -> RobotDataEstimated:
        pass

class BallTracker:
    record: OrderedDict[float, List[BallDataRaw]]
    capacity: int
    filter: StatusEstimater

    def __init__(self, filter: StatusEstimater, limit=500):
        self.record = OrderedDict()
        self.capacity = limit
        self.filter = filter

    def add(self, ball_data: BallDataRaw):
        if len(self.record) == self.capacity:
            self.record.popitem(last=False)
        time = ball_data.time_stamp
        if time in self.record:
            self.record[time].append(ball_data)
        else:
            self.record[time] = [ball_data]

    def get(self):
        return self.filter.ball_filter(self.record)


class RobotTracker:
    record: OrderedDict[float, List[RobotDataRaw]]
    capacity: int
    filter: StatusEstimater

    def __init__(self, filter: StatusEstimater, limit=100):
        self.record = OrderedDict()
        self.capacity = limit
        self.filter = filter

    def add(self, robot_data: RobotDataEstimated):
        # if it is full, remove the oldest one
        if len(self.record) == self.capacity:
            self.record.popitem(last=False)
        time = robot_data.time_stamp
        if time in self.record:
            self.record[time].append(robot_data)
        else:
            self.record[time] = [robot_data]

    def get(self):
        return self.filter.robot_filter(self.record)
