from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from ..world.world import FilteredDataWrapper

# Avoid circular import
if TYPE_CHECKING:
    from ..player import Target


class Role(ABC):
    """Abstract class for roles."""

    @abstractmethod
    def get_fitness_for_player(self, id: int, data: FilteredDataWrapper) -> float:
        """Returns a fitness value for the player with the given ID."""
        pass

    @abstractmethod
    def get_next_target(self, data: FilteredDataWrapper) -> "Target":
        """Called on fixed intervals, issues a target to the player."""
        pass
