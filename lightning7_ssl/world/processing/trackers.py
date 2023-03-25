from collections import OrderedDict
from typing import List

from . import BallDataRaw, RobotDataRaw, StatusEstimator


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
    filter: StatusEstimator

    def __init__(self, filter: StatusEstimator, limit=500):
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
    filter: StatusEstimator

    def __init__(self, filter: StatusEstimator, limit=100):
        """
        init the tracker

        Args:
            filter:  the filter strategy
            limit:  the capacity of the storage
        """
        self.record = OrderedDict()
        self.capacity = limit
        self.filter = filter

    def add(self, robot_data: RobotDataRaw):
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
