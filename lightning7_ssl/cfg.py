from typing import Literal

from .utils import ConfigLoader

# Use this file to store global variables. This is a good place to keep
# the world object, or a config object for example.


# Global configuration variables
class GlobalConfig(ConfigLoader):
    """Global configuration variables.

    Attributes:
        tick_interval_sec: The interval between ticks in seconds.
        team_color: The team color.
        num_players: The number of players on the team.
        vision_host: The host to receive vision data from.
        vision_port: The port to receive vision data from.
        command_local_host: The hostname from which to send commands, must be on the same network as the remote.
        command_remote_host: The hostname to send commands to.
        command_remote_port: The port to send commands to.
        ui: Whether to run the browser UI or not.
        ui_host: The host to run the UI on, defaults to localhost (only used if ui is True).
        ui_port: The port to run the UI on, defaults to 5173 or another available port (only used if ui is True).
        open_browser: Whether to open the browser or not (only used if ui is True).
        log_file: The pickle file to dump logs to.
    """

    tick_interval_sec: float = 0.1
    team_color: Literal["blue", "yellow"] = "blue"
    num_players: int = 11

    vision_host: str = "224.5.23.2"
    vision_port: int = 10020
    command_local_host: str = "127.0.0.1"
    command_remote_host: str = "127.0.0.1"
    command_remote_port: int = 10301

    ui: bool = False
    ui_host: str = "localhost"
    ui_port: int = 5173
    open_browser: bool = False
    log_file: str = "logs.pickle"
