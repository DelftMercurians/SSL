from typing import List
from dataclasses import dataclass
import numpy as np

from .pathfinder import find_path
from ..stratcore import Goal
from ..control_client import SSLClient, RobotData

# Margin of error when arriving at a target location
TARGET_TRESHOLD = 10


class Status:
    """Player status enum"""

    class Idle:
        pass

    @dataclass
    class Moving:
        target: np.ndarray


# Player status type for typechecker
PlayerStatus = Status.Idle | Status.Moving


class Player:
    """Responsible for controlling a single robot and executing goals from the startegy."""

    client: SSLClient

    id: int
    pos_loaded: bool = False
    pos: np.ndarray
    vel: np.ndarray
    status: PlayerStatus
    goal_stack: List[Goal]

    def __init__(self, id: int, client: SSLClient):
        self.id = id
        self.client = client
        self.pos = np.zeros(2)
        self.vel = np.zeros(2)
        self.status = Status.Idle()
        self.goal_stack = []

    def recv_update(self, state: RobotData):
        """Update the player's internal state."""
        if not self.pos_loaded and state.x == state.y == 0:
            return

        self.pos_loaded = True
        self.pos[0] = state.x
        self.pos[1] = state.y
        # TODO: compute velocity

        # Update status based on new state
        if isinstance(self.status, Status.Moving):
            dist = np.linalg.norm(self.status.target - self.pos)
            if dist <= TARGET_TRESHOLD:
                # Reached goal
                self._process_next_goal()

    def tick(self):
        """Called on fixed intervals, should move to execute current goal."""
        if isinstance(self.status, Status.Moving):
            dir_x, dir_y = find_path(self.pos, self.status.target)
            self._move(dir_x, dir_y)
        elif isinstance(self.status, Status.Idle):
            self._move(0, 0)

    def append_goal(self, goal: Goal, high_priority=False):
        if high_priority:
            self.goal_stack.insert(0, goal)
        else:
            self.goal_stack.append(goal)
        self._process_next_goal()

    # Internal methods
    # ------------------------------------

    def _process_next_goal(self):
        if len(self.goal_stack) > 0:
            next_goal = self.goal_stack.pop()
            # TODO: Check for type of goal
            print(f"{self.id} got goal {next_goal.targetPos}")
            self.status = Status.Moving(next_goal.targetPos)
        else:
            self.status = Status.Idle()

    def _move(self, velX: float = 0, velY: float = 0, yaw: float = 0):
        self.client.send(self.id, velX, velY, yaw)
