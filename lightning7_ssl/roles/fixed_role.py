from ..vecMath.vec_math import Vec2
from ..player.player import Target
from ..world.world import FilteredDataWrapper
from . import Role


class FixedRole(Role):
    """A role that always assigns the same target to the player."""

    def __init__(self, target_pos: Vec2):
        self.target = Target(move_to=target_pos)

    def get_fitness_for_player(self, _: int, __: FilteredDataWrapper) -> float:
        return 1

    def get_next_target(self, _: FilteredDataWrapper) -> Target:
        return self.target
