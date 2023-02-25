from typing import Optional
from dataclasses import dataclass
import numpy as np

from .pathfinder import find_path
from lightning7_ssl.World.maintainer import World
from ..control_client import SSLClient

# Margin of error when arriving at a target location
TARGET_TRESHOLD = 10


@dataclass
class Target:
    """A single target, dispatched from a role to a player.

    Attributes:
        player: ID of the recipient robot
        target_pos: Target position
    """

    player: int
    move_to: Optional[np.ndarray] = None


class Status:
    """Player status enum"""

    class Idle:
        pass

    @dataclass
    class Moving:
        target: np.ndarray


# Player status type for typechecker
PlayerStatus = Status.Idle | Status.Moving


# TODO: Move state management to World object and query robot state from there
class Player:
    """Responsible for controlling a single robot and executing targets from the role."""

    client: SSLClient

    id: int
    pos_loaded: bool = False
    pos: np.ndarray
    status: PlayerStatus

    def __init__(self, id: int, client: SSLClient):
        self.id = id
        self.client = client
        self.pos = np.zeros(2)
        self.status = Status.Idle()

    def set_target(self, target: Target):
        """Set a new target for this player."""
        if target.move_to is None:
            self.status = Status.Idle()
        else:
            self.status = Status.Moving(target.move_to)

    def tick(self, data: World):
        """Called on fixed intervals, should move to execute current target."""
        state = next((r for r in data.own_robots if r.id == self.id), None)
        if state is None or (not self.pos_loaded and state.x == state.y == 0):
            return

        self.pos_loaded = True
        self.pos[0] = state.x
        self.pos[1] = state.y

        # Update status based on new state
        if isinstance(self.status, Status.Moving):
            dist = np.linalg.norm(self.status.target - self.pos)
            if dist <= TARGET_TRESHOLD:
                # Reached target
                self.status = Status.Idle()

        if isinstance(self.status, Status.Moving):
            dir_x, dir_y = find_path(self.pos, self.status.target)
            self._move(dir_x, dir_y)
        elif isinstance(self.status, Status.Idle):
            self._move(0, 0)

    # Internal methods
    # -----------------------------------

    def _move(self, velX: float = 0, velY: float = 0, yaw: float = 0):
        self.client.send(self.id, velX, velY, yaw)
