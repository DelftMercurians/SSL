import unittest

from lightning7_ssl.logtool.Gamelog import Gamelog
from lightning7_ssl.logtool.log_player import LogPlayer


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        g = Gamelog.from_binary("../logs/testt_goal_2.log")
        self.player = LogPlayer(g.headers, g.data, 0.5)

    def test_play(self):
        self.player.play()


if __name__ == "__main__":
    unittest.main()
