from dataclasses import dataclass, field
from typing import Tuple
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


