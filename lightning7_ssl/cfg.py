from typing import Literal

from .vis.data_store import DataStore
from .world import World

# Use this file to store global variables. This is a good place to keep
# the world object, or a config object for example.

# Configuration variables with default values
tick_interval_sec: float = 0.1
team_color: Literal["blue", "yellow"] = "blue"
num_players: int = 11

# Global objects
world: World = None  # type: ignore
data_store: DataStore = None  # type: ignore


def setup_globals(
    num_players_on_field: int,
    own_team_color: Literal["blue", "yellow"],
    tick_interval: float = 0.1,
) -> None:
    """Setup the global variables. This should be called before any other
    function in the codebase.

    Use this function to configure the global variables.

    Args:
        num_robots: The number of robots on the team.
        own_team: The team color.
        tick_interval: The interval between ticks in seconds.
    """
    global team_color  # pylint: disable=global-statement
    global num_players  # pylint: disable=global-statement
    global tick_interval_sec  # pylint: disable=global-statement
    team_color = own_team_color
    num_players = num_players_on_field
    tick_interval_sec = tick_interval

    global world  # pylint: disable=global-statement
    global data_store  # pylint: disable=global-statement
    data_store = DataStore()
    world = World(
        num_robots=num_players_on_field,
        is_blue=own_team_color == "blue",
        update_geom_only_once=True,
    )
