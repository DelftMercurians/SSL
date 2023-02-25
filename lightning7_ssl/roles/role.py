from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from lightning7_ssl.World.world import World

# Avoid circular import
if TYPE_CHECKING:
    from ..player import Target


class Role(ABC):
    """Abstract class for roles."""

    @abstractmethod
    def get_fitness_for_player(self, id: int, data: World) -> float:
        """Returns a fitness value for the player with the given ID."""
        pass

    @abstractmethod
    def get_next_target(self, data: World) -> "Target":
        """Called on fixed intervals, issues a target to the player."""
        pass
