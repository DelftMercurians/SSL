from typing import List
import numpy as np
from dataclasses import dataclass
from common import RobotTracker, BallTracker

class World:
    """Represents the current state of the world."""
    def __init__(self, num_robots = 7, is_blue = True):
        self.own_robots = []
        self.opp_robots: []
        self.ball = BallTracker()

    @staticmethod
    def from_vision_data(data: VisionData, own_team: str):
        return World(
            own_robots=data.blue_robots if own_team == "blue" else data.yellow_robots,
            opp_robots=data.yellow_robots if own_team == "blue" else data.blue_robots,
            ball=np.array([data.ball.x, data.ball.y]),
        )
