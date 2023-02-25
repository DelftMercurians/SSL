from time import time
from multiprocessing import Process

from .control_client import SSLClient
from .player import PlayerManager
from lightning7_ssl.world.maintainer import *
from .vis.generate_log import LogGenerator
from .vis.world_plotter import WorldPlotter

TICK_INTERVAL_SEC = 0.1
OWN_TEAM = "blue"
NUM_PLAYERS = 11

# Field info
DIV = "A"
LENGTH = 12
WIDTH = 9
RADIUS_ROBOT = 0.0793
world = World(NUM_PLAYERS, OWN_TEAM == "blue")
logger = LogGenerator("test.pickle")
plotter = WorldPlotter("test.pickle")


def main():
    print("Starting test server")
    with SSLClient() as client:
        player_manager = PlayerManager(NUM_PLAYERS, client)

        # Ping the server to start the game
        client.send(0, 0, 0)

        last_tick = time()
        while True:
            vision_data = client.receive()
            current_time = time()
            if (
                current_time - last_tick >= TICK_INTERVAL_SEC
                and vision_data is not None
            ):
                data_filtered = World.update_vision_data(vision_data)
                logger.step(data_filtered)
                player_manager.tick(data_filtered)
                last_tick = current_time


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Generate log file then plot it
        logger.generate()
        # plotter.plot()
        # plotter.play()
