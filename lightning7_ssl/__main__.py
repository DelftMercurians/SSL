import argparse
from time import time
from typing import Optional

from . import cfg
from .control_client import SSLClient
from .player import PlayerManager
from .roles.fixed_role import FixedRole
from .vecMath.vec_math import Vec2
from .vis.generate_log import LogGenerator
from .web.server import ServerWrapper


def main(ui: bool = False, log_file: Optional[str] = None) -> None:
    web_server = ServerWrapper(open_browser=ui, ui_dev_server=ui)
    cfg.data_store.subscribe(web_server.step)
    if log_file is not None:
        logger = LogGenerator("logs.pickle")
        cfg.data_store.subscribe(logger.step)
    with SSLClient() as client:
        player_manager = PlayerManager(client)

        # Ping the server to start the game
        client.send(0, 0, 0)

        last_tick = time()

        while True:
            vision_data = client.receive()
            cfg.world.update_from_protobuf(vision_data)

            if time() - last_tick >= cfg.tick_interval_sec:
                ball_state = cfg.world.get_ball_state()
                if ball_state is not None:
                    ball_pos = ball_state.position
                    if len(player_manager.assigned_roles) == 0:
                        player_manager.spawn_role(
                            FixedRole(Vec2(ball_pos.x, ball_pos.y)),
                        )

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
    parser = argparse.ArgumentParser()
    parser.prog = "lightning7_ssl"
    parser.add_argument(
        "--ui",
        action="store_true",
        default=False,
        help="Run the browser UI",
    )
    parser.add_argument(
        "--num-players",
        type=int,
        default=11,
        help="The number of players on the field",
    )
    parser.add_argument(
        "--own-team",
        type=str,
        default="blue",
        choices=["blue", "yellow"],
        help="The team color",
    )
    parser.add_argument(
        "--tick-interval",
        type=float,
        default=0.1,
        help="The interval between ticks in seconds",
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default="logs.pickle",
        help="The file to log to",
    )
    args = parser.parse_args()

    cfg.setup_globals(
        num_players_on_field=args.num_players,
        own_team_color=args.own_team,
        tick_interval=args.tick_interval,
    )
    main(ui=args.ui, log_file=args.log_file)
