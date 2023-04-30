import bisect
import json
import struct
import zlib
from dataclasses import dataclass
from typing import List

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
            frame = SSL_Referee()
            frame.ParseFromString(data[index : index + message_size])
            index += message_size
            frames.append(frame)
        elif message_type == MESSAGE_SSL_VISION_2014 or message_type == MESSAGE_SSL_VISION_2010:
            frame = SSL_WrapperPacket()
            frame.ParseFromString(data[index : index + message_size])
            index += message_size
            frames.append(frame)
        elif message_type == MESSAGE_SSL_VISION_TRACKER_2020:
            frame = TrackerWrapperPacket()
            frame.ParseFromString(data[index : index + message_size])
            index += message_size
            frames.append(frame)
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


class Gamelog:
    """Reads and writes gamelog files."""

    data: List
    headers: List
    timeStamps: List
    GoalScenes: List
    FoulScenes: List

    def __init__(self, data: List, headers: List = []):
        self.data = data
        self.headers = headers
        self.GoalScenes = []
        self.FoulScenes = []
        self.timeStamps = []

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

    def getTimeStamps(self):
        if len(self.timeStamps) > 0:
            return self.timeStamps
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
                self.timeStamps.append(this_t - referee_time_base)
            elif isinstance(packet, SSL_WrapperPacket):
                if packet.HasField("detection"):
                    this_t = packet.detection.t_capture
                    if vision_time_base == 0:
                        vision_time_base = this_t
                    self.timeStamps.append(this_t - vision_time_base)
                else:
                    self.timeStamps.append(self.timeStamps[-1])
            elif isinstance(packet, TrackerWrapperPacket):
                source = packet.uuid
                this_t = packet.tracked_frame.timestamp
                if not tracked_time_base.__contains__(source):
                    tracked_time_base[source] = this_t
                self.timeStamps.append(this_t - tracked_time_base[source])
            else:
                self.timeStamps.append(-1)
        return self.timeStamps

    def getGoalScenes(self):
        BEFORE_LENGTH = 5
        AFTER_LENGTH = 0
        if len(self.GoalScenes) > 0:
            return self.GoalScenes
        ts = self.getTimeStamps()
        scoreb = 0
        scorey = 0
        for i in range(len(self.data)):
            packet = self.data[i]
            if isinstance(packet, SSL_Referee):
                if packet.yellow.score < scorey or packet.blue.score < scoreb:
                    if len(self.GoalScenes) > 0:
                        self.GoalScenes.remove(self.GoalScenes[-1])
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
                    self.GoalScenes.append((start_index, end_index))
                scoreb = packet.blue.score
                scorey = packet.yellow.score
        return self.GoalScenes

    def getFoulScenes(self):
        BEFORE_LENGTH = 5
        AFTER_LENGTH = 1
        if len(self.FoulScenes) > 0:
            return self.FoulScenes
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
                    self.FoulScenes.append((reasons, (start_index, end_index)))
                foul_count_yellow = foul_yellow_now
                foul_count_blue = foul_blue_now
        return self.FoulScenes
