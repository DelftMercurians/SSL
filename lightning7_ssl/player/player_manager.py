from typing import List, Dict, Type
from ..control_client import SSLClient
from ..world.maintainer import FilteredDataWrapper, World
from ..roles import Role
from .player import Player, Target


class PlayerManager:
    """Creates a player instance for each of our robots on the field,
    assigns roles and dispatches targets.

    Attributes:
        players: A dictionary of player ids to player instances.
        assigned_roles: A dictionary of player ids to roles.
        client: The client to send commands to.
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

    def tick(self, world: World):
        """Called on fixed intervals, should move all players."""
        data = world.get_status()
        for id, player in self.players.items():
            role = self.assigned_roles.get(player.id)
            if role:
                target = role.get_next_target(data)
                player.set_target(target)
            else:
                # No role assigned, idle
                player.set_target(Target(move_to=None))
            state = data.own_robots_status[id]
            if state is not None:
                player.tick(state, world)
            # TODO: Reevaluate role fitness

    def spawn_role(self, new_role: Role, data: FilteredDataWrapper):
        """Spawn a new role and assign it to a player.

        Args:
            new_role: The role to spawn.
            data: The current world state.
        """
        unassigned_players = [
            id for id in self.players.keys() if id not in self.assigned_roles
        ]
        if len(unassigned_players) == 0:
            # No unassigned players, find the least fit player
            least_fit_player = min(
                self.players,
                key=lambda id: self.assigned_roles[id].get_fitness_for_player(id, data),
            )
            self.assigned_roles[least_fit_player] = new_role
        else:
            # Assign to the most fit available player
            most_fit_player = max(
                unassigned_players,
                key=lambda id: new_role.get_fitness_for_player(id, data),
            )
            self.assigned_roles[most_fit_player] = new_role
