import unittest
from lightning7_ssl.World.maintainer import World, filteredDataWrapper
from lightning7_ssl.control_client.protobuf.ssl_detection_pb2 import SSL_DetectionFrame
from lightning7_ssl.World.common import *
class frameGenerator:
    def __init__(self):
        self.frame = SSL_DetectionFrame()
        self.frame.camera_id = 0
        self.frame.t_capture = 0

    def add_ball(self, x, y, z, confidence):
        ball = self.frame.balls.add()
        ball.x = x
        ball.y = y
        ball.z = z
        ball.confidence = confidence

    def add_robot(self, robot_id, x, y, orientation, is_yellow):
        robot = self.frame.robots_yellow.add() if is_yellow else self.frame.robots_blue.add()
        robot.robot_id = robot_id
        robot.x = x
        robot.y = y
        robot.orientation = orientation

    def get_frame(self):
        return self.frame

class EstimationGenerator:
    def __init__(self):
        own_team = [None, None, None, None, None, None, None]
        opp_team = [None, None, None, None, None, None, None]
        ball_status = None
        self.estimation = filteredDataWrapper(ball_status, own_team, opp_team)


    def update_ball(self, pos:Vector3,speed:Vector3):
        self.estimation.ball_status = BallDataEstimated(pos,speed)

    def update_robot(self, robot_id, pos:Vector2, orientation, speed:Vector2, angular_speed, is_yellow):
        robot = self.estimation.opp_robots_status if is_yellow else self.estimation.own_robots_status
        robot[robot_id] = RobotDataEstimated(pos, orientation, speed, angular_speed)

    def get_estimation(self):
        return self.estimation


class MyTestCase(unittest.TestCase):
    def test_empty(self):
        world = World()
        t = str(world.get_status())
        self.assertEqual(t,str(EstimationGenerator().get_estimation()))


    def test_complex(self):
        world = World()
        expected = EstimationGenerator()
        #data preperation
        #init status
        frame = frameGenerator()
        f = float(0.0)
        frame.add_ball(f,f,f,f)
        expected.update_ball((f,f,f),(f,f,f))
        for i in range(7):
            frame.add_robot(i,-1.0,i,0,True)#opp team
            frame.add_robot(i,1.0,i,0,False)#own team
            expected.update_robot(i,(1.0,float(i)),0.0,(f,f),0.0,False)
            expected.update_robot(i,(-1.0,float(i)),0.0,(f,f),0.0,True)
        res = str(world.update_vision_data(frame.get_frame()))
        #print type of expected estimation
        print(type(expected.get_estimation()))










if __name__ == '__main__':
    unittest.main()
