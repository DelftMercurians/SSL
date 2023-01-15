from abc import ABC, abstractmethod
from typing import List
from .common import Context, Goal


class Strategy(ABC):
    """Base class for all strategies.

    Attributes:
        is_active: Whether this is currently the active strategy
    """

    is_active: bool

    @abstractmethod
    def get_fitness(self, ctx: Context) -> float:
        """Determines how well the strategy could handle the current situation.

        Called every tick for every inactive strategy.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_moves(self, ctx: Context) -> List[Goal]:
        """Returns the list of commands to be dispatched this tick."""
        raise NotImplementedError()
