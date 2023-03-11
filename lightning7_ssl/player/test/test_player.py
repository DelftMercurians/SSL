import unittest
from unittest.mock import MagicMock, patch
from lightning7_ssl.player.player import Player, Status, Target
from lightning7_ssl.vecMath.vec_math import Vec2
from lightning7_ssl.world.maintainer import FilteredDataWrapper
from lightning7_ssl.world.common import BallDataEstimated, RobotDataEstimated


@patch("lightning7_ssl.player.player.SSLClient")
class PlayerTestSuite(unittest.TestCase):
    def test_player_moves_towards_target(self, mock_client: MagicMock):
        # Target to (0, 100)
        target = Target(0, Vec2(0, 100))
        player = Player(0, mock_client)
        player.set_target(target)
        self.assertEqual(player.status.target[0], 0)
        self.assertEqual(player.status.target[1], 100)
        mock_world = MagicMock()
        mock_world.get_team_position.return_value = [
            Vec2(0, 0),
        ]
        mock_world.get_opp_position.return_value = [
            Vec2(0, 0),
        ]
        mock_world.get_team_vel.return_value = [
            Vec2(0, 0),
        ]
        mock_world.get_opp_vel.return_value = [
            Vec2(0, 0),
        ]
        player.tick(RobotDataEstimated(Vec2(0, 0), 0, Vec2(0, 0), 0), mock_world)
        # Velocity should be (0, 1)
        mock_client.send.assert_called_with(0, 0, 1, 0)

    def test_player_stops_at_target(self, mock_client: MagicMock):
        # Target to (0, 0)
        target = Target(0, Vec2(0, 0))
        player = Player(0, mock_client)
        player.set_target(target)
        mock_world = MagicMock()
        mock_world.get_team_position.return_value = [
            Vec2(0, 0),
        ]
        mock_world.get_opp_position.return_value = [
            Vec2(0, 0),
        ]
        mock_world.get_team_vel.return_value = [
            Vec2(0, 0),
        ]
        mock_world.get_opp_vel.return_value = [
            Vec2(0, 0),
        ]
        player.tick(RobotDataEstimated(Vec2(0, 0), 0, Vec2(0, 0), 0), mock_world)
        self.assertIsInstance(player.status, Status.Idle)


if __name__ == "__main__":
    unittest.main()
