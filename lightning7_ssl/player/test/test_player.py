import unittest
from typing import cast
from unittest.mock import MagicMock, patch

from lightning7_ssl.player.player import Player, Status, Target
from lightning7_ssl.vecMath.vec_math import Vec2


@patch("lightning7_ssl.player.player.SSLClient")
@patch("lightning7_ssl.cfg.world")
class PlayerTestSuite(unittest.TestCase):
    def test_player_moves_towards_target(self, mock_client: MagicMock, mock_world: MagicMock):
        # Target to (0, 100)
        target = Target(Vec2(0, 100))
        player = Player(0, mock_client)
        player.set_target(target)
        self.assertTrue(isinstance(player.status, Status.Moving))

        status = cast(Status.Moving, player.status)
        self.assertEqual(status.target[0], 0)
        self.assertEqual(status.target[1], 100)
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
        player.tick()
        # Velocity should be (0, 1)
        mock_client.send.assert_called_with(0, 0, 1, 0)

    def test_player_stops_at_target(self, mock_client: MagicMock, mock_world: MagicMock):
        # Target to (0, 0)
        target = Target(Vec2(0, 0))
        player = Player(0, mock_client)
        player.set_target(target)
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
        player.tick()
        self.assertIsInstance(player.status, Status.Idle)


if __name__ == "__main__":
    unittest.main()
