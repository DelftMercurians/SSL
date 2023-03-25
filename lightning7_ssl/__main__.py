import argparse
from time import time
from typing import Literal

from . import cfg
from .control_client import SSLClient
from .player import PlayerManager
from .roles.fixed_role import FixedRole
from .vecMath.vec_math import Vec2
from .vis.generate_log import LogGenerator
from .web.server import ServerWrapper

TICK_INTERVAL_SEC = 0.1
OWN_TEAM: Literal["blue", "yellow"] = "blue"
NUM_PLAYERS = 11

# Field info
DIV = "A"
LENGTH = 12
WIDTH = 9
RADIUS_ROBOT = 0.0793
logger = LogGenerator("logs.pickle")


def main(force_dev=False):
    web_server = ServerWrapper(force_dev_mode=force_dev)
    cfg.data_store.subscribe(logger.step)
    cfg.data_store.subscribe(web_server.step)
    with SSLClient() as client:
        player_manager = PlayerManager(NUM_PLAYERS, client)

        # Ping the server to start the game
        client.send(0, 0, 0)

        last_tick = time()

        while True:
            vision_data = client.receive()
            cfg.world.update_from_protobuf(vision_data)

            if time() - last_tick >= TICK_INTERVAL_SEC:
                ball_state = cfg.world.get_ball_state()
                if ball_state is not None:
                    ball_pos = ball_state.position
                    print(f"Ball location: {ball_pos}")
                    player_manager.spawn_role(
                        FixedRole(Vec2(ball_pos.x, ball_pos.y)),
                    )

                player_manager.tick()
                last_tick = time()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dev",
        action="store_true",
        default=False,
        help="Run the server in development mode",
    )
    args = parser.parse_args()
    cfg.setup_globals(num_robots=NUM_PLAYERS, own_team=OWN_TEAM)
    main(force_dev=args.dev)
