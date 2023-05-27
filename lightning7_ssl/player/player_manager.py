from typing import Dict

from lightning7_ssl.world import WorldCtx

from ..cfg import GlobalConfig
from ..control_client import SSLClient
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
    ctx: WorldCtx

    def __init__(self, client: SSLClient, ctx: WorldCtx, config: GlobalConfig) -> None:
        """Create a new player manager.

        Args:
            client: The client to send commands to.
        """
        self.client = client
        self.ctx = ctx
        self.assigned_roles = {}
        self.players = {id: Player(id, client) for id in range(config.num_players)}

    def tick(self):
        """Called on fixed intervals, should move all players."""
        frame = self.ctx.last_frame
        for player in self.players.values():
            role = self.assigned_roles.get(player.id)
            if role:
                target = role.get_next_target()
                player.set_target(target)
            else:
                # No role assigned, idle
                player.set_target(Target(move_to=None))
            player.tick(frame)
            # TODO: Reevaluate role fitness

    def spawn_role(self, new_role: Role):
        """Spawn a new role and assign it to a player.

        Args:
            new_role: The role to spawn.
            data: The current world state.
        """
        unassigned_players = [id for id in self.players.keys() if id not in self.assigned_roles]
        if len(unassigned_players) == 0:
            # No unassigned players, find the least fit player
            least_fit_player = min(
                self.players,
                key=lambda id: self.assigned_roles[id].get_fitness_for_player(id),
            )
            self.assigned_roles[least_fit_player] = new_role
        else:
            # Assign to the most fit available player
            most_fit_player = max(
                unassigned_players,
                key=lambda id: new_role.get_fitness_for_player(id),
            )
            self.assigned_roles[most_fit_player] = new_role
