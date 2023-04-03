from dataclasses import dataclass
from typing import Optional

from lightning7_ssl.vecMath.vec_math import Vec2

from .. import cfg
from ..control_client import SSLClient
from .pathfinder import find_path

# Margin of error when arriving at a target location
TARGET_TRESHOLD = 50


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

    def tick(self):
        """Called on fixed intervals, should move to execute current target."""
        pos = cfg.world.get_robot_pos(self.id)
        heading = cfg.world.get_robot_heading(self.id)  # -90 deg = East
        if isinstance(self.status, Status.Moving):
            dist = (self.status.target - pos).norm
            if dist <= TARGET_TRESHOLD:
                # Reached target
                self.status = Status.Idle()
            else:
                # Move towards target
                speed = dist / 1000
                dir = find_path(self.id, self.status.target) * speed
                # Convert to robot coordinates
                # TODO: Should this be elsewhere?
                local_vel = dir.rotate_axis(heading)
                self._move(local_vel)
        if isinstance(self.status, Status.Idle):
            # Stop moving
            self._move()

    # Internal methods
    # -----------------------------------

    def _move(self, local_vel: Vec2 = Vec2(), yaw: float = 0):
        self.client.send(self.id, local_vel.x, local_vel.y, yaw)
