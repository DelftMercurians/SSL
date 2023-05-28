from time import time

from . import cfg
from .control_client import SSLClient
from .player import PlayerManager

# from .roles.fixed_role import FixedRole
# from .vecMath.vec_math import Vec2
from .vis.generate_log import LogGenerator
from .web.server import ServerWrapper
from .playground2.playground import MatchMaker
from .control_client.protobuf.ssl_wrapper_pb2 import SSL_WrapperPacket

# from .vis.vector_field import draw_vector_field
# from .player.pathfinder import find_path


def main() -> None:
    if cfg.config.ui:
        web_server = ServerWrapper(
            ui_dev_server=True,
            open_browser=cfg.config.open_browser,
            ui_host=cfg.config.ui_host,
            ui_port=cfg.config.ui_port,
        )
        cfg.data_store.subscribe(web_server.step)
    if cfg.config.log_file is not None:
        logger = LogGenerator("logs.pickle")
        cfg.data_store.subscribe(logger.step)
    with SSLClient() as client:
        player_manager = PlayerManager(client)

        # Ping the server to start the game
        client.send(0, 0, 0)

        vision_data = client.receive()
        cfg.world.update_from_protobuf(vision_data)
        geo = SSL_WrapperPacket()
        geo.ParseFromString(vision_data)
        match_maker = MatchMaker(
            client,
            [9.0, -5.0],
            {0: [1.0, 5.0], 1: [5.3, 5.1], 2: [5.3, 0.0], 3: [5.3, -5.1], 4: [1.0, -5.0], 5: [1.0, 0.0]},
            geo.geometry,
        )
        match_maker.reset()
        last_tick = time()

        while True:
            vision_data = client.receive()
            cfg.world.update_from_protobuf(vision_data)

            if time() - last_tick >= cfg.config.tick_interval_sec:
                ball_state = cfg.world.get_ball_state()
                if ball_state is not None:
                    ball_pos = ball_state.position
                    print(ball_pos)
                    # if len(player_manager.assigned_roles) == 0:
                    #     player_manager.spawn_role(
                    #         FixedRole(Vec2(ball_pos.x, ball_pos.y)),
                    #     )

                    # if cfg.world.field_geometry:
                    #     # Draw a vector field for the ball
                    #     vec_field = draw_vector_field(
                    #         (
                    #             cfg.world.field_geometry.field_width,
                    #             cfg.world.field_geometry.field_length,
                    #         ),
                    #         lambda pos: find_path(0, ball_pos.to_vec2(), start_pos=pos),
                    #     )
                    #     cfg.data_store.update_vector_field(vec_field)

                player_manager.tick()

                last_tick = time()


if __name__ == "__main__":
    cfg.setup_globals(parser_prog="python -m lightning7_ssl")
    main()
