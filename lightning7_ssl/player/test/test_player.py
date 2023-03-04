import unittest
import numpy as np
from unittest.mock import MagicMock, patch
from lightning7_ssl.player.player import Player, Status, Target
from lightning7_ssl.world.maintainer import FilteredDataWrapper
from lightning7_ssl.world.common import BallDataEstimated, RobotDataEstimated


@patch("lightning7_ssl.player.player.SSLClient")
class PlayerTestSuite(unittest.TestCase):
    def test_player_moves_towards_target(self, mock_client: MagicMock):
        # Target to (0, 100)
        target = Target(0, np.array([0, 100]))
        player = Player(0, mock_client)
        player.set_target(target)
        self.assertEqual(player.status.target[0], 0)
        self.assertEqual(player.status.target[1], 100)
        player.tick(RobotDataEstimated((0, 0), 0, (0, 0), 0))
        # Velocity should be (0, 1)
        mock_client.send.assert_called_with(0, 0, 1, 0)

    def test_player_stops_at_target(self, mock_client: MagicMock):
        # Target to (0, 0)
        target = Target(0, np.array([0, 0]))
        player = Player(0, mock_client)
        player.set_target(target)
        player.tick(RobotDataEstimated((0, 0), 0, (0, 0), 0))
        self.assertIsInstance(player.status, Status.Idle)


if __name__ == "__main__":
    unittest.main()
