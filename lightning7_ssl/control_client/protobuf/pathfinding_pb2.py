# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pathfinding.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x11pathfinding.proto\x12\x0bpathfinding"\x1e\n\x06Vector\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02"5\n\x0e\x43ircleObstacle\x12#\n\x06\x63\x65nter\x18\x01 \x01(\x0b\x32\x13.pathfinding.Vector"`\n\x0cRectObstacle\x12(\n\x0b\x62ottom_left\x18\x01 \x01(\x0b\x32\x13.pathfinding.Vector\x12&\n\ttop_right\x18\x02 \x01(\x0b\x32\x13.pathfinding.Vector"u\n\x10TriangleObstacle\x12\x1f\n\x02p1\x18\x01 \x01(\x0b\x32\x13.pathfinding.Vector\x12\x1f\n\x02p2\x18\x02 \x01(\x0b\x32\x13.pathfinding.Vector\x12\x1f\n\x02p3\x18\x03 \x01(\x0b\x32\x13.pathfinding.Vector"T\n\x0cLineObstacle\x12"\n\x05start\x18\x01 \x01(\x0b\x32\x13.pathfinding.Vector\x12 \n\x03\x65nd\x18\x02 \x01(\x0b\x32\x13.pathfinding.Vector"\xaa\x01\n\x14MovingCircleObstacle\x12&\n\tstart_pos\x18\x01 \x01(\x0b\x32\x13.pathfinding.Vector\x12"\n\x05speed\x18\x02 \x01(\x0b\x32\x13.pathfinding.Vector\x12 \n\x03\x61\x63\x63\x18\x03 \x01(\x0b\x32\x13.pathfinding.Vector\x12\x12\n\nstart_time\x18\x04 \x01(\x02\x12\x10\n\x08\x65nd_time\x18\x05 \x01(\x02"\x9c\x02\n\x12MovingLineObstacle\x12\'\n\nstart_pos1\x18\x01 \x01(\x0b\x32\x13.pathfinding.Vector\x12#\n\x06speed1\x18\x02 \x01(\x0b\x32\x13.pathfinding.Vector\x12!\n\x04\x61\x63\x63\x31\x18\x03 \x01(\x0b\x32\x13.pathfinding.Vector\x12\'\n\nstart_pos2\x18\x04 \x01(\x0b\x32\x13.pathfinding.Vector\x12#\n\x06speed2\x18\x05 \x01(\x0b\x32\x13.pathfinding.Vector\x12!\n\x04\x61\x63\x63\x32\x18\x06 \x01(\x0b\x32\x13.pathfinding.Vector\x12\x12\n\nstart_time\x18\x07 \x01(\x02\x12\x10\n\x08\x65nd_time\x18\x08 \x01(\x02"e\n\x0fTrajectoryPoint\x12 \n\x03pos\x18\x01 \x01(\x0b\x32\x13.pathfinding.Vector\x12"\n\x05speed\x18\x02 \x01(\x0b\x32\x13.pathfinding.Vector\x12\x0c\n\x04time\x18\x03 \x01(\x02"O\n\x15\x46riendlyRobotObstacle\x12\x36\n\x10robot_trajectory\x18\x01 \x03(\x0b\x32\x1c.pathfinding.TrajectoryPoint"c\n\x15OpponentRobotObstacle\x12&\n\tstart_pos\x18\x01 \x01(\x0b\x32\x13.pathfinding.Vector\x12"\n\x05speed\x18\x02 \x01(\x0b\x32\x13.pathfinding.Vector"\xef\x03\n\x08Obstacle\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04prio\x18\x02 \x01(\x05\x12\x0e\n\x06radius\x18\x03 \x01(\x02\x12-\n\x06\x63ircle\x18\x04 \x01(\x0b\x32\x1b.pathfinding.CircleObstacleH\x00\x12.\n\trectangle\x18\x05 \x01(\x0b\x32\x19.pathfinding.RectObstacleH\x00\x12\x31\n\x08triangle\x18\x06 \x01(\x0b\x32\x1d.pathfinding.TriangleObstacleH\x00\x12)\n\x04line\x18\x07 \x01(\x0b\x32\x19.pathfinding.LineObstacleH\x00\x12:\n\rmoving_circle\x18\t \x01(\x0b\x32!.pathfinding.MovingCircleObstacleH\x00\x12\x36\n\x0bmoving_line\x18\n \x01(\x0b\x32\x1f.pathfinding.MovingLineObstacleH\x00\x12<\n\x0e\x66riendly_robot\x18\x0b \x01(\x0b\x32".pathfinding.FriendlyRobotObstacleH\x00\x12<\n\x0eopponent_robot\x18\x0c \x01(\x0b\x32".pathfinding.OpponentRobotObstacleH\x00\x42\n\n\x08obstacle"\xa4\x01\n\nWorldState\x12(\n\tobstacles\x18\x01 \x03(\x0b\x32\x15.pathfinding.Obstacle\x12\x1d\n\x15out_of_field_priority\x18\x02 \x01(\r\x12+\n\x08\x62oundary\x18\x03 \x01(\x0b\x32\x19.pathfinding.RectObstacle\x12\x0e\n\x06radius\x18\x04 \x01(\x02\x12\x10\n\x08robot_id\x18\x05 \x01(\r"\xbe\x01\n\x0fTrajectoryInput\x12\x1f\n\x02v0\x18\x01 \x01(\x0b\x32\x13.pathfinding.Vector\x12\x1f\n\x02v1\x18\x02 \x01(\x0b\x32\x13.pathfinding.Vector\x12\x1f\n\x02s0\x18\x04 \x01(\x0b\x32\x13.pathfinding.Vector\x12\x1f\n\x02s1\x18\x05 \x01(\x0b\x32\x13.pathfinding.Vector\x12\x11\n\tmax_speed\x18\x06 \x01(\x02\x12\x14\n\x0c\x61\x63\x63\x65leration\x18\x07 \x01(\x02"\x92\x01\n\x0fPathFindingTask\x12&\n\x05state\x18\x01 \x01(\x0b\x32\x17.pathfinding.WorldState\x12+\n\x05input\x18\x02 \x01(\x0b\x32\x1c.pathfinding.TrajectoryInput\x12*\n\x04type\x18\x03 \x01(\x0e\x32\x1c.pathfinding.InputSourceType"]\n\x14StandardSamplerPoint\x12\x0c\n\x04time\x18\x01 \x01(\x02\x12\r\n\x05\x61ngle\x18\x02 \x01(\x02\x12\x13\n\x0bmid_speed_x\x18\x03 \x01(\x02\x12\x13\n\x0bmid_speed_y\x18\x04 \x01(\x02"\x91\x01\n$StandardSamplerPrecomputationSegment\x12=\n\x12precomputed_points\x18\x01 \x03(\x0b\x32!.pathfinding.StandardSamplerPoint\x12\x14\n\x0cmin_distance\x18\x02 \x01(\x02\x12\x14\n\x0cmax_distance\x18\x03 \x01(\x02"d\n\x1dStandardSamplerPrecomputation\x12\x43\n\x08segments\x18\x01 \x03(\x0b\x32\x31.pathfinding.StandardSamplerPrecomputationSegment*v\n\x0fInputSourceType\x12\x08\n\x04None\x10\x00\x12\x0f\n\x0b\x41llSamplers\x10\x01\x12\x13\n\x0fStandardSampler\x10\x02\x12\x18\n\x14\x45ndInObstacleSampler\x10\x03\x12\x19\n\x15\x45scapeObstacleSampler\x10\x04'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "pathfinding_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _INPUTSOURCETYPE._serialized_start = 2521
    _INPUTSOURCETYPE._serialized_end = 2639
    _VECTOR._serialized_start = 34
    _VECTOR._serialized_end = 64
    _CIRCLEOBSTACLE._serialized_start = 66
    _CIRCLEOBSTACLE._serialized_end = 119
    _RECTOBSTACLE._serialized_start = 121
    _RECTOBSTACLE._serialized_end = 217
    _TRIANGLEOBSTACLE._serialized_start = 219
    _TRIANGLEOBSTACLE._serialized_end = 336
    _LINEOBSTACLE._serialized_start = 338
    _LINEOBSTACLE._serialized_end = 422
    _MOVINGCIRCLEOBSTACLE._serialized_start = 425
    _MOVINGCIRCLEOBSTACLE._serialized_end = 595
    _MOVINGLINEOBSTACLE._serialized_start = 598
    _MOVINGLINEOBSTACLE._serialized_end = 882
    _TRAJECTORYPOINT._serialized_start = 884
    _TRAJECTORYPOINT._serialized_end = 985
    _FRIENDLYROBOTOBSTACLE._serialized_start = 987
    _FRIENDLYROBOTOBSTACLE._serialized_end = 1066
    _OPPONENTROBOTOBSTACLE._serialized_start = 1068
    _OPPONENTROBOTOBSTACLE._serialized_end = 1167
    _OBSTACLE._serialized_start = 1170
    _OBSTACLE._serialized_end = 1665
    _WORLDSTATE._serialized_start = 1668
    _WORLDSTATE._serialized_end = 1832
    _TRAJECTORYINPUT._serialized_start = 1835
    _TRAJECTORYINPUT._serialized_end = 2025
    _PATHFINDINGTASK._serialized_start = 2028
    _PATHFINDINGTASK._serialized_end = 2174
    _STANDARDSAMPLERPOINT._serialized_start = 2176
    _STANDARDSAMPLERPOINT._serialized_end = 2269
    _STANDARDSAMPLERPRECOMPUTATIONSEGMENT._serialized_start = 2272
    _STANDARDSAMPLERPRECOMPUTATIONSEGMENT._serialized_end = 2417
    _STANDARDSAMPLERPRECOMPUTATION._serialized_start = 2419
    _STANDARDSAMPLERPRECOMPUTATION._serialized_end = 2519
# @@protoc_insertion_point(module_scope)
