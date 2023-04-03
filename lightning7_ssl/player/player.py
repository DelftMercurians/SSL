from dataclasses import dataclass
from typing import Dict, Optional

from lightning7_ssl.vecMath.vec_math import Vec2

from .. import cfg
from ..control_client import SSLClient
from .pathfinder import find_path

# Margin of error when arriving at a target location
TARGET_TRESHOLD = 10


@dataclass
class Target:
    """A single target, dispatched from a role to a player.

    Attributes:
        move_to: Target position
    """

    move_to: Optional[Vec2] = None


class Status:
    """Player status enum"""

    class Idle:
        pass

    @dataclass
    class Moving:
        target: Vec2

    @staticmethod
    def to_json(status: "PlayerStatus") -> Dict:
        """Convert a player status to a JSON string."""
        if isinstance(status, Status.Idle):
            return {"type": "idle"}
        elif isinstance(status, Status.Moving):
            return {"type": "moving", "target": status.target}
        else:
            raise ValueError("Unknown player status type.")


# Player status type for typechecker
PlayerStatus = Status.Idle | Status.Moving


# TODO: Move state management to World object and query robot state from there
class Player:
    """Responsible for controlling a single robot and executing targets from the role."""

    client: SSLClient

    id: int
    status: PlayerStatus

    def __init__(self, id: int, client: SSLClient):
        self.id = id
        self.client = client
        self.status = Status.Idle()

    def set_target(self, target: Target):
        """Set a new target for this player."""
        if target.move_to is None:
            self.status = Status.Idle()
        else:
            self.status = Status.Moving(target.move_to)
        cfg.data_store.update_player_state(self)

    def tick(self):
        """Called on fixed intervals, should move to execute current target."""
        pos = cfg.world.get_robot_pos(self.id)
        if isinstance(self.status, Status.Moving):
            dist = (self.status.target - pos).norm
            if dist <= TARGET_TRESHOLD:
                # Reached target
                self.status = Status.Idle()
                cfg.data_store.update_player_state(self)
            else:
                # Move towards target
                dir_x, dir_y = find_path(self.id, self.status.target)
                self._move(dir_x, dir_y)
        if isinstance(self.status, Status.Idle):
            # Stop moving
            self._move(0, 0)

    # Internal methods
    # -----------------------------------

    def _move(self, velX: float = 0, velY: float = 0, yaw: float = 0):
        self.client.send(self.id, velX, velY, yaw)
