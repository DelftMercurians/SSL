from typing import List, Dict, Type

from ..control_client import SSLClient
from lightning7_ssl.world.maintainer import FilteredDataWrapper, World
from ..roles import Role
from .player import Player, Target


class PlayerManager:
    """Creates a player instance for each of our robots on the field,
    assigns roles and dispatches targets.

    Args:
        player_ids: Either the number of players or a list of their IDs.
    """

    players: Dict[int, Player]
    assigned_roles: Dict[int, Role]
    client: SSLClient

    def __init__(self, player_ids: int | List[int], client: SSLClient) -> None:
        self.client = client
        self.assigned_roles = {}
        self.players = {
            id: Player(id, client)
            for id in (
                player_ids if isinstance(player_ids, list) else range(player_ids)
            )
        }

    def tick(self, data: FilteredDataWrapper):
        """Called on fixed intervals, should move all players."""
        for id, player in self.players.items():
            role = self.assigned_roles.get(player.id)
            if role:
                target = role.get_next_target(data)
                player.set_target(target)
            else:
                # No role assigned, idle
                player.set_target(Target(player.id, move_to=None))
            state = next((d for d in data.own_robots_status if d.id == id), None)
            if state is not None:
                player.tick(state)
            # TODO: Reevaluate role fitness

    def spawn_role(self, role: Type[Role], data: FilteredDataWrapper):
        """Spawn a new role and assign it to a player.

        Args:
            role: The type of role to spawn.
        """
        new_role = role()
        unassigned_players = [
            p for p in self.players if p.id not in self.assigned_roles
        ]
        if len(unassigned_players) == 0:
            # No unassigned players, find the least fit player
            least_fit_player = min(
                self.players,
                key=lambda p: self.assigned_roles[p.id].get_fitness_for_player(
                    p.id, data
                ),
            )
            self.assigned_roles[least_fit_player.id] = new_role
        else:
            # Assign to the most fit player
            most_fit_player = max(
                self.players, key=lambda p: new_role.get_fitness_for_player(p.id, data)
            )
            self.assigned_roles[most_fit_player.id] = new_role

    def dispatch_target(self, id: int, target: Target):
        """Deliver the target to the correct player.

        TODO: Add support for roles
        """
        player = next((p for p in self.players if p.id == id))
        player.set_target(target)
