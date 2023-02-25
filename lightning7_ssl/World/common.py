from dataclasses import dataclass, field
from typing import Tuple
from collections import OrderedDict
import abc
Vector2 = Tuple[float, float]
Vector3 = Tuple[float, float, float]
@dataclass
class RobotDataRaw:
    time_stamp: float
    camara_id: int
    position: Vector2
    orientation: float  # [-pi,pi]

    def __str__(self):
        return "RobotDataRaw: [time: " + str(self.time_stamp) + " camera: " + str(self.camara_id) + " pos: " + str(self.position) + " ori: " + str(self.orientation)+ "]\n"

@dataclass
class RobotDataEstimated:
    position: Vector2
    orientation: float
    velocity: Vector2
    angular_speed: float

    def __str__(self):
        return "RobotDataEstimated: [pos: " + str(self.position) + " ori: " + str(self.orientation) + " velocity: " + str(self.velocity) + " spin: " + str(self.angular_speed)+ "]\n"

@dataclass
class BallDataRaw:
    time_stamp: float
    camara_id: int
    position: Vector3
    confidence: float

    def __str__(self):
        return "BallDataRaw: [time: " + str(self.time_stamp) + " camera: " + str(self.camara_id) + " pos: " + str(self.position) + " confidence: " + str(self.confidence)+ "]\n"


@dataclass
class BallDataEstimated:
    position: Vector2
    velocity: Vector2

    def __str__(self):
        return "BallDataEstimated: [pos: " + str(self.position) + " velocity: " + str(self.velocity) + "]\n"



class StatusEstimater(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def ball_filter(self, raw_data: OrderedDict) -> BallDataEstimated:
        pass

    @abc.abstractmethod
    def robot_filter(self, raw_data: OrderedDict) -> RobotDataEstimated:
        pass


class BallTracker:
    def __init__(self, filter: StatusEstimater, limit = 500):
        self.record = OrderedDict(maxlen = limit)
        self.capacity = limit
        self.filter = filter

    def add(self,ball_data: BallDataRaw):
        time = ball_data.time_stamp
        if time in self.record:
            self.record[time].append(ball_data)
        else:
            self.record[time] = [ball_data]
        #if it is full, remove the oldest one
        if len(self.record) == self.capacity:
            self.record.popitem(last=False)
    def get(self):
        return filter.ball_filter(self.record)


class RobotTracker:
    def __init__(self, filter: StatusEstimater, limit = 1000):
        self.record = OrderedDict(maxlen = limit)
        self.capacity = limit
        self.filter = filter

    def add(self,robot_data: RobotDataEstimated):
        time = robot_data.time_stamp
        if time in self.record:
            self.record[time].append(robot_data)
        else:
            self.record[time] = [robot_data]
        #if it is full, remove the oldest one
        if len(self.record) == self.capacity:
            self.record.popitem(last=False)
    def get(self):
        return filter.robot_filter(self.record)
