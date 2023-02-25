from common import *
class SimpleFilter(StatusEstimater):

    def ball_filter(self, raw_data: OrderedDict) -> BallDataEstimated:
        ball_list = raw_data.items()
        if len(ball_list) == 0:
            return None

        last_candidates = ball_list[-1]
        # use the position in the candidate balls which has the highest confidence
        last_candidates.sort(key=lambda x: x.confidence, reverse=True)
        pos_this = last_candidates[0].position

        if len(ball_list) == 1:
            return BallDataEstimated(pos_this, Vector3(0,0,0))

        previous_candidates = ball_list[-2]
        # use the position in the candidate balls which has the highest confidence
        previous_candidates.sort(key=lambda x: x.confidence, reverse=True)
        pos_prev = previous_candidates[0].position

        timediff = last_candidates[0].time_stamp - previous_candidates[0].time_stamp
        velocity = (pos_this - pos_prev) / timediff
        return BallDataEstimated(pos_this, velocity)




    def robot_filter(self, raw_data: OrderedDict) -> RobotDataEstimated:
        robot_list = raw_data.items()
        if len(robot_list) == 0:
            return None

        last_candidates = robot_list[-1]
        # calculate the average position in the candidate balls
        pos_this = Vector3(0,0)
        ori = 0
        for candidate in last_candidates:
            pos_this += candidate.position
            ori += candidate.orientation

        pos_this /= len(last_candidates)
        ori /= len(last_candidates)

        if len(robot_list) == 1:
            v = Vector3(0,0)
            spinv_v = 0
        else:
            previous_candidates = robot_list[-2]
            # calculate the average position in the candidate balls
            pos_prev = Vector3(0,0)
            ori_prev = 0
            for candidate in previous_candidates:
                pos_prev += candidate.position
                ori_prev += candidate.orientation

            pos_prev /= len(previous_candidates)
            ori_prev /= len(previous_candidates)

            timediff = last_candidates[0].time_stamp - previous_candidates[0].time_stamp
            v = (pos_this - pos_prev) / timediff
            spinv_v = (ori - ori_prev) / timediff
        return RobotDataEstimated(pos_this, ori, v, spinv_v)
