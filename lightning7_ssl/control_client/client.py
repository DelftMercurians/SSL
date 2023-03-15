import socket
from dataclasses import dataclass, field
from typing import List, Optional, Set
from protobuf_to_dict import protobuf_to_dict
from google.protobuf.message import DecodeError

from .protobuf.ssl_simulation_robot_control_pb2 import RobotControl
from .protobuf.ssl_wrapper_pb2 import SSL_WrapperPacket


@dataclass
class BallData:
    x: float
    y: float
    z: float
    confidence: float

    def __str__(self):
        return (
            "BallData: [x: "
            + str(self.x)
            + " y: "
            + str(self.y)
            + " z: "
            + str(self.z)
            + " confidence: "
            + str(self.confidence)
            + "]"
        )


@dataclass
class RobotData:
    id: int
    x: float
    y: float
    yaw: float  # [-pi,pi]

    def __str__(self):
        return (
            "RobotData: [id: "
            + str(self.id)
            + " x: "
            + str(self.x)
            + " y: "
            + str(self.y)
            + " yaw: "
            + str(self.yaw)
            + "]"
        )


@dataclass
class VisionData:
    ball: Optional[BallData] = None
    blue_robots: List[RobotData] = field(default_factory=list)
    yellow_robots: List[RobotData] = field(default_factory=list)

    @staticmethod
    def from_protobuf(data: bytes):
        """Converts protobuf data to VisionData."""
        packet = SSL_WrapperPacket()
        packet.ParseFromString(data)
        frame = packet.detection
        vision_data = VisionData()
        if len(frame.balls) > 0:
            ball = frame.balls[0]
            vision_data.ball = BallData(
                x=ball.x,
                y=ball.y,
                z=ball.z,
                confidence=ball.confidence,
            )
        vision_data.blue_robots = [
            RobotData(
                id=robot.robot_id,
                x=robot.x,
                y=robot.y,
                yaw=robot.orientation,
            )
            for robot in frame.robots_blue
        ]
        vision_data.yellow_robots = [
            RobotData(
                id=robot.robot_id,
                x=robot.x,
                y=robot.y,
                yaw=robot.orientation,
            )
            for robot in frame.robots_yellow
        ]

        return vision_data

    def __str__(self):
        return (
            "VisionData:"
            + "\n"
            + str(self.ball)
            + "\n"
            + " blue_robots: \n"
            + str(self.blue_robots)
            + "\n"
            + " yellow_robots: \n"
            + str(self.yellow_robots)
        )


class SSLClient:
    """Client for sending commands and receiving vision data from a simulator."""

    known_robot_ids: Set[int]

    def __init__(
        self,
        command_ip: str = "127.0.0.1",
        command_port: int = 10301,
        vision_ip: str = "224.5.23.2",
        vision_port: int = 10020,
    ):
        self.cmd_ip = command_ip
        self.command_port = command_port
        self.vision_ip = vision_ip
        self.vision_port = vision_port
        self.known_robot_ids = set()

    def __enter__(self):
        """Binds the client with ip and port and configure to UDP multicast."""
        self.cmd_sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        )
        self.cmd_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.cmd_sock.bind((self.cmd_ip, 0))

        self.vision_sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        )
        self.vision_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.vision_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 128)
        self.vision_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        self.vision_sock.bind((self.vision_ip, self.vision_port))

        host = socket.gethostbyname(socket.gethostname())
        self.vision_sock.setsockopt(
            socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host)
        )
        self.vision_sock.setsockopt(
            socket.SOL_IP,
            socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton(self.vision_ip) + socket.inet_aton(host),
        )

        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Stop all robots and close socket."""
        for id in self.known_robot_ids:
            self.send(id, 0, 0)
        self.cmd_sock.close()

    def receive(self):
        """Receive package and decode."""
        data, _ = self.vision_sock.recvfrom(2048) # Influences how much data we get
        return data

    def send(
        self,
        id: int,
        vel_x: float,
        vel_y: float,
        angular_speed: float = 0,
        dribbler_speed: float = 0,
        kick_speed: float = 0,
        kick_angle: float = 0,
    ):
        """Send a command to a robot.

        Args:
            id: The id of the robot.
            vel_x: Velocity forward [m/s] (towards the dribbler).
            vel_y: Velocity to the left [m/s].
            angular_speed: Angular velocity counter-clockwise [rad/s]
            dribbler_speed: Dribbler speed in rounds per minute [rpm].
            kick_speed: Absolute kick speed [m/s].
            kick_angle: Kick angle [degree] (0 degrees for a straight kick).
        """
        self.known_robot_ids.add(id)
        control_msg = RobotControl()
        command = control_msg.robot_commands.add()
        command.id = id
        command.move_command.local_velocity.forward = vel_y
        command.move_command.local_velocity.left = vel_x
        command.move_command.local_velocity.angular = angular_speed
        command.dribbler_speed = dribbler_speed
        command.kick_speed = kick_speed
        command.kick_angle = kick_angle
        return self.cmd_sock.sendto(
            control_msg.SerializeToString(), (self.cmd_ip, self.command_port)
        )
