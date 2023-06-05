import bisect
import json
import struct
import zlib
from dataclasses import dataclass
from typing import List
import math
import numpy as np
from google.protobuf.json_format import MessageToDict

from lightning7_ssl.control_client.protobuf.ssl_referee_pb2 import SSL_Referee
from lightning7_ssl.control_client.protobuf.ssl_vision_wrapper_tracked_pb2 import (
    TrackerWrapperPacket,
)
from lightning7_ssl.control_client.protobuf.ssl_wrapper_pb2 import SSL_WrapperPacket

MESSAGE_BLANK = 0
MESSAGE_UNKNOWN = 1
MESSAGE_SSL_VISION_2010 = 2
MESSAGE_SSL_REFBOX_2013 = 3
MESSAGE_SSL_VISION_2014 = 4
MESSAGE_SSL_VISION_TRACKER_2020 = 5
MESSAGE_SSL_INDEX_2021 = 6
INDEX_MARKER = "INDEXED"
FOUL_REASONS = [
    "attacker_too_close_to_defense_area",
    "defender_in_defense_area",
    "boundary_crossing",
    "keeper_held_ball",
    "bot_dribbled_ball_too_far",
    "bot_pushed_bot",
    "bot_held_ball_deliberately",
    "bot_tipped_over",
    "attacker_touched_ball_in_defense_area",
    "bot_kicked_ball_too_fast",
    "bot_crash_unique",
    "bot_crash_drawn",
    "defender_too_close_to_kick_point",
    "bot_too_fast_in_stop",
    "bot_interfered_placement",
]
STOP_COMMANDS = [SSL_Referee.Command.STOP, SSL_Referee.Command.HALT]
START_COMMANDS = [SSL_Referee.Command.FORCE_START,
                  SSL_Referee.PREPARE_KICKOFF_BLUE, SSL_Referee.PREPARE_KICKOFF_YELLOW,
                  SSL_Referee.Command.DIRECT_FREE_BLUE,
                  SSL_Referee.Command.DIRECT_FREE_YELLOW, SSL_Referee.Command.INDIRECT_FREE_BLUE,
                  SSL_Referee.Command.INDIRECT_FREE_YELLOW]
MAX_ROBOT = 11 # DIVISION_A
@dataclass
class Index:
    """An index message from the log file."""

    offsets: List[int]
    offset_from_end: int
    index_marker: str

    def __init__(self):
        self.offsets = []
        self.offset_from_end = 0
        self.index_marker = ""

    def to_dict(self):
        return {
            "offsets": self.offsets,
            "offset_from_end": self.offset_from_end,
            "index_marker": self.index_marker,
        }

    def to_binary(self):
        """Returns the binary representation of this index."""
        # 7 for the marker, 8 for the offset from end
        # pack offsets, offset_from_end, index_marker
        return (
            struct.pack(f"{len(self.offsets)}q", *self.offsets)
            + struct.pack(">q", self.offset_from_end)
            + self.index_marker.encode("ascii")
        )


def get_frames(data: bytes):
    """Returns a list of objects."""

    frames: list[SSL_Referee | SSL_WrapperPacket | TrackerWrapperPacket | Index] = []
    headers = []

    index = len("SSL_LOG_FILE")
    # read an int32 from the data
    int_st = struct.Struct(">i")
    (log_type_int,) = int_st.unpack(data[index : index + int_st.size])
    index += int_st.size
    if log_type_int != 1:
        print("Not a detection frame log")
        return None

    while index < len(data):
        timestamp = struct.unpack(">q", data[index : index + 8])[0]
        index += 8
        message_type = struct.unpack(">i", data[index : index + 4])[0]
        index += 4
        message_size = struct.unpack(">i", data[index : index + 4])[0]
        index += 4
        headers.append((timestamp, message_type, message_size))
        if index + message_size > len(data):
            break
        if message_type == MESSAGE_SSL_REFBOX_2013:
            ref_frame: SSL_Referee = SSL_Referee()
            ref_frame.ParseFromString(data[index : index + message_size])
            index += message_size
            frames.append(ref_frame)
        elif message_type == MESSAGE_SSL_VISION_2014 or message_type == MESSAGE_SSL_VISION_2010:
            vis_frame: SSL_WrapperPacket = SSL_WrapperPacket()
            vis_frame.ParseFromString(data[index : index + message_size])
            index += message_size
            frames.append(vis_frame)
        elif message_type == MESSAGE_SSL_VISION_TRACKER_2020:
            track_frame: TrackerWrapperPacket = TrackerWrapperPacket()
            track_frame.ParseFromString(data[index : index + message_size])
            index += message_size
            frames.append(track_frame)
        elif message_type == MESSAGE_SSL_INDEX_2021:
            end = index + message_size
            # type: ignore
            frame_idx = Index()
            frame_idx.index_marker = data[end - 7 : end].decode("ascii")
            if frame_idx.index_marker != INDEX_MARKER:
                print("Index marker not found")
                return None
            array_size = message_size - 7 - 8  # 7 for the marker, 8 for the offset from end
            frame_idx.offsets = list(struct.unpack(f">{array_size//8}q", data[index : index + array_size]))
            frame_idx.offset_from_end = struct.unpack(
                ">q", data[index + array_size : index + array_size + 8]
            )[0]
            index += message_size
            frames.append(frame_idx)
        else:
            print("Unknown message type", message_type)
            return None

    return frames, headers

def get_score(data: List):
    """Returns the score of the game."""

    score = {"blue": 0, "yellow": 0}
    for frame in data:
        if isinstance(frame, SSL_Referee):
            if frame.command in STOP_COMMANDS:
                score["blue"] = frame.blue.score
                score["yellow"] = frame.yellow.score
    return score

class Gamelog:
    """Reads and writes gamelog files."""

    data: List
    headers: List
    time_stamps: List
    goal_scenes: List
    foul_scenes: List
    game_scenes: List
    game_score: dict
    def __init__(self, data: List, headers: List = []):
        self.data = data
        self.headers = headers
        self.goal_scenes = []
        self.foul_scenes = []
        self.time_stamps = []
        self.game_scenes = []
        self.game_statistics = get_score(self.data)

    @staticmethod
    def from_binary(path: str):
        with open(path, "rb") as f:
            rawData = f.read()
            if path.endswith(".gz"):
                z = zlib.decompressobj(15 + 32)
                rawData = z.decompress(rawData)
        exp_header = "SSL_LOG_FILE"
        act_header = rawData[: len(exp_header)].decode("ascii")
        if exp_header != act_header:
            error_msg = "Error decoding file header, got {}, when expecting {}."
            error_msg = error_msg.format(act_header, exp_header)
            print(error_msg)
            return None
        data, headers = get_frames(rawData)
        return Gamelog(data, headers)

    def to_binary(self, path: str, segment=(-1, -1)):
        print(segment)
        if self.headers is None:
            print("cannot write binary file without headers")
            return
        headers = self.headers
        data = self.data
        if segment[0] != -1 and segment[1] != -1:
            headers = headers[segment[0] : segment[1]]
            data = data[segment[0] : segment[1]]
        with open(path, "wb") as f:
            f.write("SSL_LOG_FILE".encode("ascii"))
            f.write(struct.pack(">i", 1))
            for i in range(len(data)):
                #         print(f"Writing frame {i} of {len(data)}")
                f.write(struct.pack(">q", headers[i][0]))
                f.write(struct.pack(">i", headers[i][1]))
                f.write(struct.pack(">i", headers[i][2]))
                if isinstance(data[i], Index):
                    f.write(data[i].to_binary())
                else:
                    f.write(data[i].SerializeToString())

    @staticmethod
    def from_json(path: str):
        if not path.endswith(".json"):
            print("File must be a json file")
            return None
        print("Loading json file")
        data = json.load(open(path))
        print("Converting to protobuf")
        return Gamelog(data)

    def to_json(self, path: str, data):
        with open(path, "w") as f:
            f.write("[\n")
            for i in range(len(data)):
                if isinstance(data[i], Index):
                    f.write(json.dumps(data[i].to_dict()))
                else:
                    f.write(json.dumps(MessageToDict(data[i])))
                if i < len(data) - 1:
                    f.write(",\n")
            f.write("]")

    def track_one(self, robot_id: int = 0, is_blue: bool = True):
        res = []
        for i in range(len(self.data)):
            packet = self.data[i]
            if isinstance(packet, SSL_WrapperPacket) and packet.HasField("detection"):
                t = packet.detection.t_capture
                if is_blue:
                    collection = packet.detection.robots_blue
                else:
                    collection = packet.detection.robots_yellow
                for robot in collection:
                    if robot.robot_id == robot_id:
                        res.append((t, robot.x, robot.y, i))

        return res


    def save_moving_period(self, path, track):
        # slice res into useful pieces when the robot is continously moving in larger than 1s
        period = []
        status = []
        for i in range(1, len(track)):
            j = i - 1
            while j >= 0 and track[i][0] == track[j][0]:
                j -= 1
            # ms/s
            speed = math.sqrt((track[i][1] - track[j][1]) ** 2 + (track[i][2] - track[j][2]) ** 2) \
                    / ((track[i][0] - track[j][0]))
            if speed > 100:
                status.append("MOVE")
            else:
                status.append("STOP")
        # select continuous move status larger than 1s
        i = 1
        while i < len(status):
            if status[i] == "STOP":
                i += 1
                continue
            j = i
            while j < len(status) and status[j] == "MOVE":
                j += 1
            if track[j][0] - track[i][0] > 5:
                period.append((i, j))
            i = j + 1

        for start_idx, end_idx in period:
            t = []
            x = []
            y = []
            for i in range(start_idx, end_idx):
                t.append(track[i][0])
                x.append(track[i][1])
                y.append(track[i][2])
            np.savez(path, t=t, x=x, y=y)
        return period

    def getTimeStamps(self):
        if len(self.time_stamps) > 0:
            return self.time_stamps
        if len(self.data) == 0:
            return None
        referee_time_base = 0
        vision_time_base = 0
        tracked_time_base = {}
        for i in range(len(self.data)):
            packet = self.data[i]
            if isinstance(packet, SSL_Referee):
                this_t = packet.packet_timestamp / 1000000.0
                if referee_time_base == 0:
                    referee_time_base = this_t
                self.time_stamps.append(this_t - referee_time_base)
            elif isinstance(packet, SSL_WrapperPacket):
                if packet.HasField("detection"):
                    this_t = packet.detection.t_capture
                    if vision_time_base == 0:
                        vision_time_base = this_t
                    self.time_stamps.append(this_t - vision_time_base)
                else:
                    self.time_stamps.append(self.time_stamps[-1])
            elif isinstance(packet, TrackerWrapperPacket):
                source = packet.uuid
                this_t = packet.tracked_frame.timestamp
                if not tracked_time_base.__contains__(source):
                    tracked_time_base[source] = this_t
                self.time_stamps.append(this_t - tracked_time_base[source])
            else:
                self.time_stamps.append(-1)
        return self.time_stamps

    def getGoalScenes(self):
        BEFORE_LENGTH = 5
        AFTER_LENGTH = 0
        if len(self.goal_scenes) > 0:
            return self.goal_scenes
        ts = self.getTimeStamps()
        scoreb = 0
        scorey = 0
        for i in range(len(self.data)):
            packet = self.data[i]
            if isinstance(packet, SSL_Referee):
                if packet.yellow.score < scorey or packet.blue.score < scoreb:
                    if len(self.goal_scenes) > 0:
                        self.goal_scenes.remove(self.goal_scenes[-1])
                if packet.yellow.score > scorey or packet.blue.score > scoreb:
                    # search for the first none halt command frame before this frame
                    # print("Found valid goal at frame {}".format(i))
                    # print(packet.command)
                    # print(packet.yellow.score,packet.blue.score)
                    j = i - 1
                    while j >= 0:
                        if isinstance(self.data[j], SSL_Referee):
                            if (
                                self.data[j].command != SSL_Referee.HALT
                                and self.data[j].command != SSL_Referee.STOP
                            ):
                                break
                        j -= 1
                    # print(j,self.data[j].command)

                    # print("Found possible goal at frame {}".format(j))

                    start = ts[j] - BEFORE_LENGTH
                    end = ts[j] + AFTER_LENGTH
                    start_index = bisect.bisect_left(ts, start)
                    end_index = bisect.bisect_right(ts, end)
                    self.goal_scenes.append((start_index, end_index))
                scoreb = packet.blue.score
                scorey = packet.yellow.score
        return self.goal_scenes

    def getFoulScenes(self):
        BEFORE_LENGTH = 5
        AFTER_LENGTH = 1
        if len(self.foul_scenes) > 0:
            return self.foul_scenes
        ts = self.getTimeStamps()
        foul_count_yellow = 0
        foul_count_blue = 0

        for i in range(len(self.data)):
            packet = self.data[i]
            if isinstance(packet, SSL_Referee):
                foul_yellow_now = packet.yellow.foul_counter
                foul_blue_now = packet.blue.foul_counter
                if foul_yellow_now > foul_count_yellow or foul_blue_now > foul_count_blue:
                    reasons = None
                    for game_event in packet.game_events:
                        e = game_event.WhichOneof("event")
                        if FOUL_REASONS.__contains__(e):
                            reasons = e
                    start = ts[i] - BEFORE_LENGTH
                    end = ts[i] + AFTER_LENGTH
                    start_index = bisect.bisect_left(ts, start)
                    end_index = bisect.bisect_right(ts, end)
                    self.foul_scenes.append((reasons, (start_index, end_index)))
                foul_count_yellow = foul_yellow_now
                foul_count_blue = foul_blue_now
        return self.foul_scenes

    def get_game_scenes(self):
        ts = self.getTimeStamps()
        if len(self.game_scenes) > 0:
            return self.game_scenes
        BEFORE_LENGTH = 2
        AFTER_LENGTH = 2
        sequence = []
        prev = -1
        for i in range(len(self.data)):
            packet = self.data[i]
            if isinstance(packet, SSL_Referee):
                t = packet.packet_timestamp / 1000000.0
                if packet.command in STOP_COMMANDS:
                    if prev not in STOP_COMMANDS:
                        sequence.append((t, "STOP", i))
                        prev = packet.command
                elif packet.command in START_COMMANDS:
                    if prev != packet.command:
                        sequence.append((t, "START", i))
                        prev = packet.command

        for i in range(len(sequence)):
            if sequence[i][1] == "STOP" and i>0:
                t_start = ts[sequence[i-1][2]] - BEFORE_LENGTH
                t_end = ts[sequence[i][2]] + AFTER_LENGTH


                start_index = bisect.bisect_left(ts, t_start)
                end_index = bisect.bisect_right(ts, t_end)
                self.game_scenes.append((start_index, end_index))
        # print(self.game_scenes)
        return self.game_scenes

    def save_game_track(self, folder):

        self.get_game_scenes()
        robot_postions = {}
        for p in self.game_scenes:
            for i in range(p[0], p[1]):
                packet = self.data[i]
                if isinstance(packet, SSL_WrapperPacket):
                    if packet.HasField("detection"):
                        t = packet.detection.t_capture
                        if t not in robot_postions:
                            robot_postions[t] = {}
                        for r in packet.detection.robots_blue:
                            pos = r.x, r.y
                            robot_postions[t][r.robot_id] = pos
                        for r in packet.detection.robots_yellow:
                            pos = r.x, r.y
                            robot_postions[t][r.robot_id + MAX_ROBOT] = pos
                        for ball_postion in packet.detection.balls:
                            pos = ball_postion.x, ball_postion.y, ball_postion.z
                            robot_postions[t]["ball"] = pos
            time_stamps = []
            robot_positions = []
            for key, value in robot_postions.items():
                time_stamps.append(key)
                positions = [[-10000, -10000] for i in range(MAX_ROBOT * 2)]
                for i in range(MAX_ROBOT * 2):
                    if i in value:
                        positions[i] = value[i]
                robot_positions.append(np.array(positions, dtype=np.int16))
            time_stamps = np.array(time_stamps, dtype=np.float64)
            time_stamps = np.array(time_stamps - time_stamps[0], dtype=np.float32)
            robot_positions = np.array(robot_positions, dtype=np.int16)
            np.savez_compressed(folder + "/" + str(p) + ".npz", time_stamps=time_stamps, robot_positions=robot_positions)

