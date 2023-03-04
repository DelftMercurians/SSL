from typing import Optional
from dataclasses import dataclass
import unittest
import numpy as np

from lightning7_ssl.world.common import RobotDataEstimated
from .pathfinder import find_path
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

    def tick(self, state: RobotDataEstimated):
        """Called on fixed intervals, should move to execute current target."""
        (x, y) = state.position
        if isinstance(self.status, Status.Moving):
            pos = np.asarray([x, y])
            dist = np.linalg.norm(self.status.target - pos)
            if dist <= TARGET_TRESHOLD:
                # Reached target
                self.status = Status.Idle()
            else:
                # Move towards target
                dir_x, dir_y = find_path(pos, self.status.target)
                self._move(dir_x, dir_y)
        if isinstance(self.status, Status.Idle):
            # Stop moving
            self._move(0, 0)

    # Internal methods
    # -----------------------------------

    def _move(self, velX: float = 0, velY: float = 0, yaw: float = 0):
        self.client.send(self.id, velX, velY, yaw)
