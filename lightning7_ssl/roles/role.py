from abc import ABC, abstractmethod
from ..player import Target
from ..world import World


class Role(ABC):
    """Abstract class for roles."""

    @abstractmethod
    def get_fitness_for_player(self, id: int, data: World) -> float:
        """Returns a fitness value for the player with the given ID."""
        pass

    @abstractmethod
    def get_next_target(self, data: World) -> Target:
        """Called on fixed intervals, issues a target to the player."""
        pass
