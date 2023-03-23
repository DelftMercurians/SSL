from collections import OrderedDict
from typing import List

from ...vecMath.vec_math import Vec2, Vec3
from .estimators import (
    BallDataEstimated,
    BallDataRaw,
    RobotDataEstimated,
    RobotDataRaw,
    StatusEstimator,
)


class SimpleFilter(StatusEstimator):
    """
    State estimation filter that uses the last two positions and estimates velocity.
    """

    def ball_filter(
        self, raw_data: OrderedDict[float, List[BallDataRaw]]
    ) -> BallDataEstimated:
        """
        it chooses the ball with the highest confidence and estimate the velocity based on the last two positions.

        Args:
            raw_data: a dictionary of time stamp and ball data

        Returns: the estimated ball data
        """
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
        """
        it uses the last two positions and estimate the velocity. and
        uses the last position/orientation as the final position/orientation.

        Args:
            raw_data:  a dictionary of time stamp and robot data

        Returns: the estimated robot data
        """
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

        return RobotDataEstimated(pos, ori, v, spinv)
