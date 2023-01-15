import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional


@dataclass
class Context:
    """Container for passing data between different objects.

    Attributes:
        inputs: Results of the input processing
        active_strategy: Active strategy
        strategy_fitnesses: The "fitness" of each strategy, to be used for selection
    """

    active_strategy: str
    inputs: Dict[str, str] = field(default_factory=dict)
    strategy_fitnesses: Dict[str, float] = field(default_factory=dict)


@dataclass
class Goal:
    """A single goal, dispatched from a startegy to a player (role).

    Attributes:
        player: ID of the recipient robot
    """

    player: int
    # TBD
    targetPos: Optional[np.ndarray] = None
    wheelSpeeds: Optional[Tuple[float, float, float, float]] = None
