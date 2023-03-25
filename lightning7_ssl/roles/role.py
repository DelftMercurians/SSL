from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Avoid circular import
if TYPE_CHECKING:
    from ..player import Target


class Role(ABC):
    """Abstract class for roles."""

    @abstractmethod
    def get_fitness_for_player(self, id: int) -> float:
        """Returns a fitness value for the player with the given ID."""
        pass

    @abstractmethod
    def get_next_target(self) -> "Target":
        """Called on fixed intervals, issues a target to the player."""
        pass
