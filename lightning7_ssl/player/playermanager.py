from typing import List, Dict

from ..control_client import SSLClient, RobotState
from ..stratcore.common import Goal
from .player import Player


class PlayerManager:
    """Creates a player instance for each of our robots on the field,
    assigns roles and dispatches goals.

    Args:
        player_ids: Either the number of players or a list of their IDs.
    """

    players: List[Player]
    client: SSLClient

    def __init__(self, player_ids: int | List[int], client: SSLClient) -> None:
        self.client = client
        self.players = [
            Player(id, client)
            for id in (
                player_ids if isinstance(player_ids, list) else range(player_ids)
            )
        ]

    def tick(self):
        """Called on fixed intervals, should move all players."""
        for player in self.players:
            player.tick()

    def recv_update(self, robot_states: Dict[int, RobotState]):
        """Update the players' internal states."""
        for id, upd in robot_states.items():
            player = next((p for p in self.players if p.id == id))
            player.recv_update(upd)

    def dispatch_goal(self, id: int, goal: Goal, high_priority=False):
        """Deliver the goal to the correct player.

        TODO: Add support for roles
        """
        player = next((p for p in self.players if p.id == id))
        player.append_goal(goal, high_priority)
