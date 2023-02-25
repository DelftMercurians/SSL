from typing import List
import numpy as np
from dataclasses import dataclass
from lightning7_ssl.control_client import VisionData, RobotData


@dataclass
class World:
    """Represents the current state of the world.

    Attributes:
        own_robots: List of own robots
        opp_robots: List of opponent robots
        ball: Ball position
    """

    own_robots: List[RobotData]
    opp_robots: List[RobotData]
    ball: np.ndarray

    @staticmethod
    def from_vision_data(data: VisionData, own_team: str):
        return World(
            own_robots=data.blue_robots if own_team == "blue" else data.yellow_robots,
            opp_robots=data.yellow_robots if own_team == "blue" else data.blue_robots,
            ball=np.array([data.ball.x, data.ball.y]),
        )
