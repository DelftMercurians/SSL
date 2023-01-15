import numpy as np
from time import time

from .control_client import PacketHandler, SSLClient, StrategyInfo
from .player import PlayerManager
from .stratcore.common import Goal

GRSIM_PORT = 10006
TICK_INTERVAL_SEC = 0.1
OWN_TEAM = "blue"
NUM_PLAYERS = 11

if __name__ == "__main__":
    print("Starting test server")
    with SSLClient(ip="127.0.0.1", port=GRSIM_PORT, own_team=OWN_TEAM) as client:
        strategy_info = StrategyInfo(NUM_PLAYERS)
        packet_handler = PacketHandler(strategy_info)
        player_manager = PlayerManager(NUM_PLAYERS, client)

        # Test: push a random goal
        player_manager.dispatch_goal(0, Goal(0, targetPos=np.zeros(2)))

        last_tick = time()
        while True:
            # Get update
            packet = client.receive()
            packet_handler.handle(packet)
            robot_states = (
                strategy_info.blueRobotStates
                if OWN_TEAM == "blue"
                else strategy_info.yellowRobotStates
            )
            player_manager.recv_update(robot_states)

            # Tick
            current_time = time()
            if current_time - last_tick >= TICK_INTERVAL_SEC:
                player_manager.tick()
                last_tick = current_time
