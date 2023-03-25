from typing import Literal

from .vis.data_store import DataStore
from .world import World

# Use this file to store global variables. This is a good place to keep
# the world object, or a config object for example.

world: World = None  # type: ignore
data_store: DataStore = None  # type: ignore


def setup_globals(num_robots: int, own_team: Literal["blue", "yellow"]) -> None:
    """Setup the global variables. This should be called before any other
    function in the codebase.

    Use this function to configure the global variables.

    Args:
        num_robots: The number of robots on the team.
        own_team: The team color.
    """
    global world  # pylint: disable=global-statement
    global data_store  # pylint: disable=global-statement
    data_store = DataStore()
    world = World(
        num_robots=num_robots,
        is_blue=own_team == "blue",
        update_geom_only_once=True,
    )
