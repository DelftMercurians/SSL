import socket
import numpy as np
from time import sleep, time

from .control_client import SSLClient, VisionData
from .player import PlayerManager
from .stratcore.common import Goal
from .SimpleVis.generateLog import LogGenerator
from .SimpleVis.WorldPlotter import WorldPlotter

TICK_INTERVAL_SEC = 0.1
OWN_TEAM = "blue"
NUM_PLAYERS = 11

# Field info
DIV = "A"
LENGTH = 12
WIDTH = 9
RADIUS_ROBOT = 0.0793

logger = LogGenerator('test.pickle')
plotter = WorldPlotter('test.pickle')

def main():
    print("Starting test server")
    with SSLClient() as client:
        player_manager = PlayerManager(NUM_PLAYERS, client)

        # Test: push a random goal
        player_manager.dispatch_goal(0, Goal(0, targetPos=np.zeros(2)))
        player_manager.tick()

        last_tick = time()
        while True:
            # Get update
            vision_data = client.receive()
            if vision_data is not None:
                player_manager.recv_update(
                    vision_data.blue_robots
                    if OWN_TEAM == "blue"
                    else vision_data.yellow_robots
                )
                logger.step(vision_data)

            # Tick
            current_time = time()
            if current_time - last_tick >= TICK_INTERVAL_SEC:
                player_manager.tick()
                last_tick = current_time

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Generate log file then plot it
        logger.generate()
        plotter.plot()
        plotter.play()