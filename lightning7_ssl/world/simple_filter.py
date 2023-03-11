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
            return BallDataEstimated(cur_pos, Vec3(0, 0, 0))

        previous_frame = records[-2]
        # Select reading with highest confidence
        prev_pos = sorted(previous_frame, key=lambda x: x.confidence, reverse=True)[
            0
        ].position

        timediff = current_frame[0].time_stamp - previous_frame[0].time_stamp
        velocity = (cur_pos - prev_pos) / timediff
        return BallDataEstimated(cur_pos, velocity)

    def robot_filter(
        self, raw_data: OrderedDict[float, List[RobotDataRaw]]
    ) -> RobotDataEstimated:
        records = list(raw_data.values())
        if len(records) == 0:
            return None

        current_frame = records[-1]
        # Average positions and orientations in readings from the current frame
        pos: Vec2 = sum([cand.position for cand in current_frame], Vec2()) / len(
            current_frame
        )
        ori = sum([cand.orientation for cand in current_frame]) / len(current_frame)

        v = Vec2()
        spinv = 0
        if len(records) > 1:
            previous_frame = records[-2]
            # Average positions and orientations in readings from the previous frame
            prev_pos: Vec2 = sum(
                [cand.position for cand in previous_frame],
                Vec2(),
            ) / len(previous_frame)
            prev_ori = sum([cand.orientation for cand in previous_frame]) / len(
                previous_frame
            )

            timediff = current_frame[0].time_stamp - previous_frame[0].time_stamp
            v = (pos - prev_pos) / timediff
            spinv = (ori - prev_ori) / timediff

        print("pos: ", pos, "ori: ", ori, "v: ", v, "spinv: ", spinv)
        return RobotDataEstimated(pos, ori, v, spinv)
