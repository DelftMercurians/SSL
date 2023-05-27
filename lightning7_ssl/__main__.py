from time import time

from lightning7_ssl.world.world import UninitializedError

from .cfg import GlobalConfig
from .control_client import SSLClient
from .player import PlayerManager
from .roles.fixed_role import FixedRole
from .vecMath.vec_math import Vec2
from .vis.data_store import DataStore
from .vis.generate_log import LogGenerator
from .web.server import ServerWrapper
from .world import World

# from .vis.vector_field import draw_vector_field
# from .player.pathfinder import find_path


def main(config: GlobalConfig) -> None:
    data_store = DataStore()
    world = World(data_store, config)
    if config.ui:
        web_server = ServerWrapper(
            ui_dev_server=True,
            open_browser=config.open_browser,
            ui_host=config.ui_host,
            ui_port=config.ui_port,
        )
        data_store.subscribe(web_server.step)
    if config.log_file is not None:
        logger = LogGenerator("logs.pickle")
        data_store.subscribe(logger.step)
    with SSLClient(config) as client:
        player_manager = PlayerManager(client, world.ctx, config)

        # Ping the server to start the game
        client.send(0, 0, 0)

        last_tick = time()

        while True:
            vision_data = client.receive()
            world.update_from_protobuf(vision_data)

            if time() - last_tick >= config.tick_interval_sec:
                try:
                    ball_state = world.frame().ball
                    ball_pos = ball_state.position
                    if len(player_manager.assigned_roles) == 0:
                        player_manager.spawn_role(
                            FixedRole(Vec2(ball_pos.x, ball_pos.y)),
                        )
                except UninitializedError:
                    pass

                    # if world.field_geometry:
                    #     # Draw a vector field for the ball
                    #     vec_field = draw_vector_field(
                    #         (
                    #             world.field_geometry.field_width,
                    #             world.field_geometry.field_length,
                    #         ),
                    #         lambda pos: find_path(0, ball_pos.to_vec2(), start_pos=pos),
                    #     )
                    #     data_store.update_vector_field(vec_field)

                player_manager.tick()
                last_tick = time()


if __name__ == "__main__":
    config = GlobalConfig(parser_prog="python -m lightning7_ssl")
    main(config)
