import unittest

from lightning7_ssl.control_client.protobuf.ssl_wrapper_pb2 import SSL_WrapperPacket
from lightning7_ssl.logtool.Gamelog import Gamelog


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.g: Gamelog = Gamelog.from_binary("../logs/testt_goal_1.log")

    def test_getFrame(self):
        packet = self.g.data[0]
        assert isinstance(packet, SSL_WrapperPacket)
        assert packet.detection.frame_number == 769510

    def test_json(self):
        g2 = Gamelog.from_json("../logs/test_short.json")
        packet = g2.data[0]
        assert packet["command"] == "STOP"
        assert packet["stage"] == "NORMAL_FIRST_HALF_PRE"

    def test_getTimeStamps(self):
        times = self.g.getTimeStamps()
        assert times[0] == 0
        eps = 0.1
        # assert increasing
        for i in range(1, len(times)):
            assert times[i] + eps > times[i - 1]

    def test_getScenes(self):
        g2 = Gamelog.from_binary("../logs/testt.gz")
        goals = g2.getGoalScenes()
        fouls = g2.getFoulScenes()
        expected_goals = [(70202, 73263), (122268, 125331), (576552, 579617)]
        expected_fouls = [
            ("bot_kicked_ball_too_fast", (112057, 115733)),
            ("bot_crash_unique", (118973, 122653)),
            ("bot_crash_drawn", (121798, 125476)),
            ("bot_crash_unique", (164988, 168667)),
            ("bot_crash_unique", (312796, 316474)),
            ("bot_crash_unique", (329834, 333520)),
            ("bot_interfered_placement", (339450, 343126)),
            ("bot_crash_drawn", (445023, 448698)),
            ("bot_crash_unique", (486510, 490181)),
            ("bot_crash_unique", (670317, 674000)),
            ("bot_crash_unique", (719043, 722718)),
            ("bot_interfered_placement", (719367, 723046)),
        ]
        assert goals == expected_goals
        assert fouls == expected_fouls

    def test_to_binary(self):
        print(self.g.headers[300][0] - self.g.headers[0][0])
        print(self.g.data[0])
        print(self.g.data[300])
        pass


if __name__ == "__main__":
    unittest.main()
