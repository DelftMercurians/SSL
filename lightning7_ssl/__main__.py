from time import time
from .control_client import SSLClient
from .player import PlayerManager, pathfinder
from .world.maintainer import *
from .vis.generate_log import LogGenerator
from .vis.world_plotter import WorldPlotter
from .vis.data_store import DataStore
from .vecMath.vec_math import Vec2, Vec3
import matplotlib

matplotlib.use("TkAgg")

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
                # print(vision_data)
                try:
                    data_filtered = world.update_from_protobuf(vision_data)
                    DS.update_player_and_ball_states(data_filtered)
                    pathfinder.find_path(
                        world, 0, Vec2(0, 0)
                    )  # Needs to be called after DS is updated
                    player_manager.tick(data_filtered)
                    last_tick = current_time

                except:
                    pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Generate log file then plot it
        GlobalConfig.logger.generate()
        # plotter.plot()
        # plotter.play()
