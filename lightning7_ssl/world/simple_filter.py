from .common import *


class SimpleFilter(StatusEstimater):
    """State estimation filter that uses the last two positions and estimates velocity."""

    def ball_filter(
        self, raw_data: OrderedDict[float, List[BallDataRaw]]
    ) -> BallDataEstimated:
        records = list(raw_data.values())
        if len(records) == 0:
            return None

        current_frame = records[-1]
        # Select reading with highest confidence
        cur_pos = sorted(current_frame, key=lambda x: x.confidence, reverse=True)[
            0
        ].position

        # If there is only one position reading, we cannot estimate velocity
        if len(records) == 1:
            return BallDataEstimated(cur_pos, (0, 0, 0))

        previous_frame = records[-2]
        # Select reading with highest confidence
        prev_pos = sorted(previous_frame, key=lambda x: x.confidence, reverse=True)[
            0
        ].position

        timediff = current_frame[0].time_stamp - previous_frame[0].time_stamp
        velocity = (
            (cur_pos[0] - prev_pos[0]) / timediff,
            (cur_pos[1] - prev_pos[1]) / timediff,
            (cur_pos[2] - prev_pos[2]) / timediff,
        )
        return BallDataEstimated(cur_pos, velocity)

    def robot_filter(
        self, raw_data: OrderedDict[float, List[RobotDataRaw]]
    ) -> RobotDataEstimated:
        records = list(raw_data.values())
        if len(records) == 0:
            return None

        current_frame = records[-1]
        # Average positions and orientations in readings from the current frame
        x = y = ori = 0
        for candidate in current_frame:
            x += candidate.position[0] / len(current_frame)
            y += candidate.position[1] / len(current_frame)
            ori += candidate.orientation / len(current_frame)
        v = (0, 0)
        spinv = 0
        pos_this = (x, y)
        if len(records) > 1:
            previous_frame = records[-2]
            # Average positions and orientations in readings from the previous frame
            x_prev = y_prev = ori_prev = 0
            for candidate in previous_frame:
                x_prev += candidate.position[0] / len(previous_frame)
                y_prev += candidate.position[1] / len(previous_frame)
                ori_prev += candidate.orientation / len(previous_frame)

            pos_prev = (x_prev, y_prev)
            timediff = current_frame[0].time_stamp - previous_frame[0].time_stamp
            v = (
                (pos_this[0] - pos_prev[0]) / timediff,
                (pos_this[1] - pos_prev[1]) / timediff,
            )
            spinv = (ori - ori_prev) / timediff

        return RobotDataEstimated(pos_this, ori, v, spinv)
