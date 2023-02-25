from lightning7_ssl.World.common import *
class SimpleFilter(StatusEstimater):

    def ball_filter(self, raw_data: OrderedDict) -> BallDataEstimated:
        ball_list = list(raw_data.values())
        if len(ball_list) == 0:
            return None

        last_candidates = ball_list[-1]
        # use the position in the candidate balls which has the highest confidence
        last_candidates.sort(key=lambda x: x.confidence, reverse=True)
        pos_this = last_candidates[0].position

        if len(ball_list) == 1:
            return BallDataEstimated(pos_this, (0,0,0))

        previous_candidates = ball_list[-2]
        # use the position in the candidate balls which has the highest confidence
        previous_candidates.sort(key=lambda x: x.confidence, reverse=True)
        pos_prev = previous_candidates[0].position

        timediff = last_candidates[0].time_stamp - previous_candidates[0].time_stamp
        velocity = ((pos_this[0] - pos_prev[0]) / timediff, (pos_this[1] - pos_prev[1]) / timediff\
            , (pos_this[2] - pos_prev[2]) / timediff)
        return BallDataEstimated(pos_this, velocity)




    def robot_filter(self, raw_data: OrderedDict) -> RobotDataEstimated:
        robot_list = list(raw_data.values())
        if len(robot_list) == 0:
            return None

        last_candidates = robot_list[-1]
        # calculate the average position in the candidate balls
        x = 0
        y = 0
        ori = 0

        for candidate in last_candidates:
            x += candidate.position[0]/len(last_candidates)
            y += candidate.position[1]/len(last_candidates)
            ori += candidate.orientation/len(last_candidates)
        v = (0,0)
        spinv = 0
        pos_this = (x,y)
        if len(robot_list) > 1:
            previous_candidates = robot_list[-2]
            # calculate the average position in the candidate balls
            x_prev = 0
            y_prev = 0
            ori_prev = 0
            for candidate in previous_candidates:
                x_prev += candidate.position[0]/len(previous_candidates)
                y_prev += candidate.position[1]/len(previous_candidates)
                ori_prev += candidate.orientation/len(previous_candidates)

            pos_prev = (x_prev,y_prev)
            timediff = last_candidates[0].time_stamp - previous_candidates[0].time_stamp
            v = ((pos_this[0] - pos_prev[0]) / timediff, (pos_this[1] - pos_prev[1]) / timediff)
            spinv = (ori - ori_prev) / timediff

        return RobotDataEstimated(pos_this, ori, v, spinv)
