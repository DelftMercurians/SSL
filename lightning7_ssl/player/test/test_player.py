import unittest
import numpy as np
from unittest.mock import MagicMock, patch
from lightning7_ssl.player.player import Player, Status, Target
from lightning7_ssl.world.maintainer import FilteredDataWrapper
from lightning7_ssl.world.common import BallDataEstimated, RobotDataEstimated


def get_mock_world_data():
    return FilteredDataWrapper(
        ball_status=BallDataEstimated((0, 0, 0), (0, 0, 0)),
        own_robots_status=[RobotDataEstimated(0, (0, 0), 0, (0, 0), 0)],
        opp_robots_status=[],
    )


@patch("lightning7_ssl.player.player.SSLClient")
class PlayerTestSuite(unittest.TestCase):
    def test_player_moves_towards_target(self, mock_client: MagicMock):
        # Target to (0, 1)
        target = Target(0, np.array([0, 1]))
        player = Player(0, mock_client)
        player.set_target(target)
        self.assertEqual(player.status.target[0], 0)
        self.assertEqual(player.status.target[1], 1)
        player.tick(get_mock_world_data())
        # Velocity should be (0, 1)
        mock_client.send.assert_called_with(0, 0, 1, 0)

    def test_player_stops_at_target(self, mock_client: MagicMock):
        # Target to (0, 0)
        target = Target(0, np.array([0, 0]))
        player = Player(0, mock_client)
        player.set_target(target)
        player.tick(get_mock_world_data())
        self.assertIsInstance(player.status, Status.Idle)
