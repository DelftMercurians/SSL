from time import time
from .control_client import SSLClient
from .player import PlayerManager
from lightning7_ssl.world.maintainer import *
from .config import GlobalConfig

def main():
    print("Starting test server")
    with SSLClient() as client:
        player_manager = PlayerManager(GlobalConfig.NUM_PLAYERS, client)

        # Ping the server to start the game
        client.send(0, 0, 0)

        last_tick = time()
        while True:
            vision_data = client.receive()
            current_time = time()
            if (
                current_time - last_tick >= GlobalConfig.TICK_INTERVAL_SEC
                and vision_data is not None
            ):
                data_filtered = World.update_vision_data(vision_data)
                GlobalConfig.logger.step(data_filtered)
                player_manager.tick(data_filtered)
                last_tick = current_time


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Generate log file then plot it
        GlobalConfig.logger.generate()
        # plotter.plot()
        # plotter.play()
