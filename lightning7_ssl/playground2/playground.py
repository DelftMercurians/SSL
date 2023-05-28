from ..control_client import SSLClient
from ..control_client.protobuf.ssl_game_controller_common_pb2 import BotId
from ..control_client.protobuf.ssl_geometry_pb2 import SSL_GeometryData
from ..control_client.protobuf.ssl_simulation_control_pb2 import SimulatorCommand
import socket
from typing import List, Dict

"""
    This script is to test the path planning algorithm.
    The MatchMaker class will set up the positiosn of the robots and ball.
    Different scenarios should be easily created and loaded into the simulator for testing.
"""


class MatchMaker:
    """
    Set up initial positions of robots and ball. Can be extended to reset the scenario or start
    """

    def __init__(
        self,
        client: SSLClient,
        ball: List[float],
        players: Dict[int, List[float]],
        geometry: SSL_GeometryData,
    ) -> None:
        self.client = client
        self.local_teleport_ip = "127.0.0.1"
        self.remote_teleport_ip = "127.0.0.1"
        self.remote_teleport_port = 10300

        self.teleport_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.teleport_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.teleport_sock.bind((socket.gethostbyname(self.local_teleport_ip), 0))

        # Define teleport messages for the ball
        self.packet = SimulatorCommand()
        self.packet.control.teleport_ball.x = ball[0]
        self.packet.control.teleport_ball.y = ball[1]
        self.packet.control.teleport_ball.z = 0.0

        self.packet.config.geometry.CopyFrom(geometry)

        # Define teleport messages for the robots
        for player_id in players:
            botid = BotId()
            botid.id = player_id

            # Define x and y coordinates for each robot, orientation ignored for now
            player_msg = self.packet.control.teleport_robot.add()
            player_msg.id.id = player_id
            player_msg.x = players[player_id][0]
            player_msg.y = players[player_id][1]

    def reset(self) -> None:
        """
        Reset the scenario
        """
        print(self.packet)

        out = self.teleport_sock.sendto(
            self.packet.SerializeToString(),
            (socket.gethostbyname(self.remote_teleport_ip), self.remote_teleport_port),
        )
        print(out, len(self.packet.SerializeToString()))
        # data = self.teleport_sock.recv(2048)
        # response = SimulatorCommand()
        # response.ParseFromString(data)
        # print(response.control.teleport_ball)
        # self.teleport_sock.close()
